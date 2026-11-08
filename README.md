# Pix2Text Instance
This is a Python FastAPI server that internally runs Pix2Text. The end goal is to allow OCR of text containing mathematical formulas even when the text is in Catalan (which Pix2Text does not support).

It also has a layout model, table recognition besidese the MFD (Math Formula Detection), MFR (Math Formula Recognition) and PaddleOCR v3 (for text recognition of English, Spanish and Catalan). The frontend is Vite React compiled to static files that the Python server
serves.

The server imports the local [`Pix2Text`](./Pix2Text) (forked repo added as a subdirectory). Keep that
directory in the repository (.git folder was removed to avoid being detected as a git submodule). It contains the main modification which is replacing EasyOCR with PaddleOCR for text.

## The models

The key models are MFR-1.5 and MFD-1.5 which are open source and the core contributions of breezedeus/pix2text.

They are not state of the art OCR, the good ones need to be payed. But for simple formulas they work decently well.

Git does not track model files. Pix2Text downloads models from Hugging Face
when needed. To download the MFR-1.5 ONNX model yourself, run:

```bash
source /opt/pix2text/venv/bin/activate
hf download breezedeus/pix2text-mfr-1.5 \
  --local-dir /opt/pix2text/models/1.1/mfr-1.5-onnx
```

The MFR-1.5 repository includes `encoder_model.onnx`, `decoder_model.onnx`,
and the tokenizer and processor files. The MFD-1.5 model is on
[Hugging Face](https://huggingface.co/breezedeus/pix2text-mfd-1.5).

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

Check that the response includes `"text_ocr": "paddleocr"` and
`"languages": "en,es,ca"`. PaddleOCR 3 downloads its language model the first
time it runs.

For mixed text and formula recognition, formula detection uses a confidence
threshold of `0.55`. This keeps inline equations without detecting many false positives. The text recognition is PaddleX directly (not the whole Paddle pipeline).

The first request is always slower because it loads the CPU models. Later requests
reuse them, and as models are cached (in my case in `/home/marti/.paddlex`) they persist even after page refreshes. To set the cache location in
the systemd service, add:

```ini
Environment=PADDLE_PDX_CACHE_HOME=/home/marti/.paddlex
```

The typical time for a paragraph with formulas is 15-20s, which is not optimal but hey, it's free and open source running on a i5 CPU and no GPU.

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

## License
[MIT](/LICENSE)
