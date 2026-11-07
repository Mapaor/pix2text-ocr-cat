# Pix2Text Instance
This is a python fastapi server that internally runs pix2text, allowing OCR of mathematical formulas with the open source models YOLO (layout detection), Table recognition, MFD (Math Formula Detection), MFR (Math Formula Recognition) and EasyOCR (for text recognition). The frontend is vite react compiled to static files that the python server serves.

## The models
The key models ara MFR-1.5 and MFD-1.5 which are open source and the core contributions of breezedeus/pix2text.

They are not state of the art OCR, the good ones need to be payed. But for simple formulas they work decently well.

## Development

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