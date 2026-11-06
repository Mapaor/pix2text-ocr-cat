### notes to self

After updating the server.py source code simply do:

```bash
sudo systemctl restart pix2text.service
```

Frontend changes require:

```bash
cd app/frontend
npm run build
sudo systemctl restart pix2text.service
```
