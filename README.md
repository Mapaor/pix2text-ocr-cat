# Pix2Text Instance
This is a Python FastAPI server that internally runs Pix2Text, allowing OCR
of mathematical formulas with open-source layout, table, formula detection
and recognition models. Text recognition uses PaddleOCR 3 for English, Spanish,
and Catalan.
The frontend is Vite React compiled to static files that the Python server
serves.

The server imports the local [`Pix2Text`](./Pix2Text) source tree. Keep that
directory in the repository; it contains the PaddleOCR integration used by the
server.

## The models

The key models are MFR-1.5 and MFD-1.5 which are open source and the core contributions of breezedeus/pix2text.

They are not state of the art OCR, the good ones need to be payed. But for simple formulas they work decently well.

Model weights are runtime assets and are ignored by Git. Pix2Text normally
downloads models automatically from Hugging Face. To download the MFR-1.5
ONNX model manually:

```bash
source /opt/pix2text/venv/bin/activate
hf download breezedeus/pix2text-mfr-1.5 \
  --local-dir /opt/pix2text/models/1.1/mfr-1.5-onnx
```

The MFR-1.5 repository contains `encoder_model.onnx`, `decoder_model.onnx`,
and the tokenizer and processor configuration files required for inference.
The MFD-1.5 model is available from
[breezedeus/pix2text-mfd-1.5](https://huggingface.co/breezedeus/pix2text-mfd-1.5).

## Development

### Activating the environment

```bash
source /opt/pix2text/venv/bin/activate
```

### Installing the local Pix2Text package

From `pix2text-server`, install the server dependencies and the local package:

```bash
pip install -r Pix2Text/requirements.txt
pip install -e Pix2Text
```

After restarting the service, verify the configured OCR backend:

```bash
curl http://127.0.0.1:8000/health
```

The response should report `"text_ocr": "paddleocr"` and
`"languages": "en,es,ca"`. PaddleOCR 3 downloads the language model on first
use. Mixed text/formula recognition uses a higher formula-detection confidence
threshold to avoid interpreting ordinary Catalan letters as formulas.

### Updating

After updating the server.py source do:

```bash
sudo systemctl restart pix2text.service
```

After updating the frontend, first generate the static files:

```bash
cd app/frontend
npm run build
```

And then update the server:

```bash
sudo systemctl restart pix2text.service
```

## Roadmap


## License
[MIT](/LICENSE)