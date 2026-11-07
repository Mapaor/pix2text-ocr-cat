# Pix2Text Instance
This is a python fastapi server that internally runs pix2text, allowing OCR of mathematical formulas with the open source models YOLO (layout detection), Table recognition, MFD (Math Formula Detection), MFR (Math Formula Recognition) and EasyOCR (for text recognition). The frontend is vite react compiled to static files that the python server serves.

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