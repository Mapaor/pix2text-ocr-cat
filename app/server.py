import asyncio
import io
import logging
import os
import tempfile
from pathlib import Path
from typing import Annotated, Literal

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image, UnidentifiedImageError

os.environ.setdefault("PIX2TEXT_HOME", "/opt/pix2text/models")

from pix2text import Pix2Text


MAX_UPLOAD_BYTES = 20 * 1024 * 1024
STATIC_DIR = Path(__file__).parent / "static"
INFERENCE_LIMIT = asyncio.Semaphore(1)

P2T_CONFIG = {
    "layout": {"model_type": "DocYoloLayoutParser"},
    "text_formula": {
        "mfd": {"model_name": "mfd-1.5", "model_backend": "onnx"},
        "formula": {"model_name": "mfr-1.5", "model_backend": "onnx"},
        "text": {"engine": "paddleocr"},
    },
    "table": {},
}

app = FastAPI(title="Pix2Text")
logger = logging.getLogger(__name__)
P2T_BY_LANGUAGE: dict[str, Pix2Text] = {}
app.mount("/assets", StaticFiles(directory=STATIC_DIR / "assets"), name="assets")


def get_pix2text(language: Literal["en", "es", "ca"]) -> Pix2Text:
    if language not in P2T_BY_LANGUAGE:
        config = {
            **P2T_CONFIG,
            "text_formula": {
                **P2T_CONFIG["text_formula"],
                "languages": [language],
            },
        }
        P2T_BY_LANGUAGE[language] = Pix2Text.from_config(
            total_configs=config,
            enable_formula=True,
            enable_table=True,
            device="cpu",
        )
    return P2T_BY_LANGUAGE[language]


@app.get("/", response_class=FileResponse)
async def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.head("/")
async def index_head() -> None:
    return None


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "text_ocr": "paddleocr", "languages": "en,es,ca"}


@app.post("/api/convert")
async def convert(
    image: Annotated[UploadFile, File(description="Image to convert")],
    language: Annotated[Literal["en", "es", "ca"], Form()] = "en",
    recognition_type: Annotated[
        Literal["page", "text_formula", "formula", "text"], Form()
    ] = "text_formula",
) -> dict[str, str]:
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(status_code=415, detail="Only image uploads are supported.")

    content = await image.read(MAX_UPLOAD_BYTES + 1)
    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="Image exceeds the 20 MiB upload limit.")

    try:
        with Image.open(io.BytesIO(content)) as source:
            converted = source.convert("RGB")
    except (UnidentifiedImageError, OSError) as exc:
        raise HTTPException(status_code=400, detail="The uploaded file is not a valid image.") from exc

    async with INFERENCE_LIMIT:
        try:
            pix2text = get_pix2text(language)
            result = await asyncio.to_thread(
                pix2text.recognize,
                converted,
                file_type=recognition_type,
                resized_shape=768,
                return_text=True,
            )
            if recognition_type == "page":
                to_markdown = getattr(result, "to_markdown", None)
                if not callable(to_markdown):
                    raise TypeError("Pix2Text page recognition returned an invalid result.")
                with tempfile.TemporaryDirectory() as output_dir:
                    markdown = await asyncio.to_thread(
                        to_markdown, output_dir
                    )
            else:
                markdown = result
        except (OSError, RuntimeError, TypeError, ValueError) as exc:
            logger.exception("Pix2Text recognition failed")
            raise HTTPException(status_code=500, detail="Pix2Text failed to recognize the image.") from exc

    if not isinstance(markdown, str):
        raise HTTPException(status_code=500, detail="Pix2Text returned an unexpected result.")
    return {"markdown": markdown}
