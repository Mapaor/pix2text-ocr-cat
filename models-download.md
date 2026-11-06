# Various Models

**Pix2Text (P2T)** integrates a number of different models, mainly including:

- **Layout Analysis Model**: [breezedeus/pix2text-layout](https://huggingface.co/breezedeus/pix2text-layout) ([China Mirror](https://hf-mirror.com/breezedeus/pix2text-layout)).
- **Table Recognition Model**: [breezedeus/pix2text-table-rec](https://huggingface.co/breezedeus/pix2text-table-rec) ([China Mirror](https://hf-mirror.com/breezedeus/pix2text-table-rec)).
- **Text Recognition Engine**: Supports **`80+` languages**, such as **English, Simplified Chinese, Traditional Chinese, Vietnamese**, etc. Among them, **English** and **Simplified Chinese** recognition use the open-source OCR tool [CnOCR](https://github.com/breezedeus/cnocr), while other languages use the open-source OCR tool [EasyOCR](https://github.com/JaidedAI/EasyOCR).
- **Mathematical Formula Detection Model (MFD)**: [breezedeus/pix2text-mfd-1.5](https://huggingface.co/breezedeus/pix2text-mfd-1.5) ([China Mirror](https://hf-mirror.com/breezedeus/pix2text-mfd-1.5)). Implemented based on [CnSTD](https://github.com/breezedeus/cnstd).
- **Mathematical Formula Recognition Model (MFR)**: [breezedeus/pix2text-mfr-1.5](https://huggingface.co/breezedeus/pix2text-mfr-1.5) ([China Mirror](https://hf-mirror.com/breezedeus/pix2text-mfr-1.5)).

Many of these models come from other open-source authors; we are very grateful for their contributions.

Under normal circumstances, these models will be downloaded automatically (this may be slow; as long as no error is reported, please do not interrupt the download process manually). However, if the download fails, you can refer to the instructions below for manual download.

In addition to the basic models, Pix2Text also provides the following advanced paid versions of the models:

- MFD and MFR paid models: For details, refer to [P2T Detailed Information | Breezedeus.com](https://www.breezedeus.com/article/pix2text_cn).
- CnOCR paid models: For details, refer to [CnOCR Detailed Information | Breezedeus.com](https://www.breezedeus.com/article/cnocr).

For specific instructions, please see the end of this page.

The instructions below mainly apply to the free basic models.

## Layout Analysis Model
**Layout Analysis Model** download address: [breezedeus/pix2text-layout](https://huggingface.co/breezedeus/pix2text-layout) (if you cannot access the internet freely, please use the [China Mirror](https://hf-mirror.com/breezedeus/pix2text-layout)).
Download all files here to the `~/.pix2text/1.1/layout-parser` directory (on Windows, place them in `C:\Users\<username>\AppData\Roaming\pix2text\1.1\layout-parser`). If the directory does not exist, please create it yourself.

> Note: The `1.1` in the path above is the version number of pix2text; `1.1.*` all correspond to `1.1`. If it is a different version, please replace it accordingly.

## Table Recognition Model
**Table Recognition Model** download address: [breezedeus/pix2text-table-rec](https://huggingface.co/breezedeus/pix2text-table-rec) (if you cannot access the internet freely, please use the [China Mirror](https://hf-mirror.com/breezedeus/pix2text-table-rec)).
Download all files here to the `~/.pix2text/1.1/table-rec` directory (on Windows, place them in `C:\Users\<username>\AppData\Roaming\pix2text\1.1\table-rec`). If the directory does not exist, please create it yourself.

> Note: The `1.1` in the path above is the version number of pix2text; `1.1.*` all correspond to `1.1`. If it is a different version, please replace it accordingly.

## Mathematical Formula Detection Model (MFD)
### `pix2text >= 1.1.1`
Starting from **V1.1.1**, Pix2Text's **Mathematical Formula Detection Model** download address is: [breezedeus/pix2text-mfd](https://huggingface.co/breezedeus/pix2text-mfd) (if you cannot access the internet freely, please use the [China Mirror](https://hf-mirror.com/breezedeus/pix2text-mfd)).

### `pix2text < 1.1.1`
The **Mathematical Formula Detection Model** (MFD) comes from the mathematical formula detection model (MFD) of [CnSTD](https://github.com/breezedeus/cnstd). Please refer to its code repository for instructions.

If the system cannot successfully download the model files automatically, you need to manually download them from the [**cnstd-cnocr-models**](https://huggingface.co/breezedeus/cnstd-cnocr-models) project ([China Mirror](https://hf-mirror.com/breezedeus/cnstd-cnocr-models)), or download the corresponding zip file from [Baidu Cloud Disk](https://pan.baidu.com/s/1zDMzArCDrrXHWL0AWxwYQQ?pwd=nstd) (extraction code: `nstd`) and place it in the `~/.cnstd/1.2` directory (on Windows, `C:\Users\<username>\AppData\Roaming\cnstd\1.2`).

## Mathematical Formula Recognition Model (MFR)
**Mathematical Formula Recognition Model** download address: [breezedeus/pix2text-mfr](https://huggingface.co/breezedeus/pix2text-mfr) (if you cannot access the internet freely, please use the [China Mirror](https://hf-mirror.com/breezedeus/pix2text-mfr)).
Download all files here to the `~/.pix2text/1.1/mfr-1.5-onnx` directory (on Windows, place them in `C:\Users\<username>\AppData\Roaming\pix2text\1.1\mfr-1.5-onnx`). If the directory does not exist, please create it yourself.

> Note: The `1.1` in the path above is the version number of pix2text; `1.1.*` all correspond to `1.1`. If it is a different version, please replace it accordingly.

## Text Recognition Engine
Pix2Text's **Text Recognition Engine** can recognize **`80+` languages**, such as **English, Simplified Chinese, Traditional Chinese, Vietnamese**, etc. Among them, **English** and **Simplified Chinese** recognition use the open-source OCR tool [CnOCR](https://github.com/breezedeus/cnocr), while other languages use the open-source OCR tool [EasyOCR](https://github.com/JaidedAI/EasyOCR).

Under normal circumstances, CnOCR's models will be downloaded automatically. If automatic download is not possible, you can refer to the instructions below for manual download.
CnOCR's open-source models are all placed in the [**cnstd-cnocr-models**](https://huggingface.co/breezedeus/cnstd-cnocr-models) project ([China Mirror](https://hf-mirror.com/breezedeus/cnstd-cnocr-models)) and can be downloaded and used for free.
If the download is too slow, you can also download from [Baidu Cloud Disk](https://pan.baidu.com/s/1RhLBf8DcLnLuGLPrp89hUg?pwd=nocr), with extraction code `nocr`. For specific methods, please refer to [CnOCR Online Documentation / Usage](https://cnocr.readthedocs.io/zh-cn/latest/usage).

The text detection engine in CnOCR uses [CnSTD](https://github.com/breezedeus/cnstd).
If the system cannot successfully download the model files automatically, you need to manually download them from the [**cnstd-cnocr-models**](https://huggingface.co/breezedeus/cnstd-cnocr-models) project ([China Mirror](https://hf-mirror.com/breezedeus/cnstd-cnocr-models)), or download the corresponding zip file from [Baidu Cloud Disk](https://pan.baidu.com/s/1zDMzArCDrrXHWL0AWxwYQQ?pwd=nstd) (extraction code: `nstd`) and place it in the `~/.cnstd/1.2` directory (on Windows, `C:\Users\<username>\AppData\Roaming\cnstd\1.2`).

For more information about CnOCR models, please refer to [CnOCR Online Documentation / Available Models](https://cnocr.readthedocs.io/zh-cn/latest/models).

CnOCR also provides **advanced paid models**. For details, refer to the instructions at the end of this article.

- CnOCR paid models: For details, refer to [CnOCR Detailed Information | Breezedeus.com](https://www.breezedeus.com/article/cnocr).

<br/>

For EasyOCR model downloads, please refer to [EasyOCR](https://github.com/JaidedAI/EasyOCR).

## Advanced Paid Models

In addition to the basic models, Pix2Text also provides the following advanced paid versions of the models:

- MFD and MFR paid models: For details, refer to [P2T Detailed Information | Breezedeus.com](https://www.breezedeus.com/article/pix2text_cn).
- CnOCR paid models: For details, refer to [CnOCR Detailed Information | Breezedeus.com](https://www.breezedeus.com/article/cnocr).

> Note that paid models include different license versions. Please refer to the specific product description when purchasing.

Before purchasing, it is recommended to first use the **[Online Demo](https://huggingface.co/spaces/breezedeus/Pix2Text-Demo)** (if you cannot access the internet freely, you can use the [China Demo](https://hf-mirror.com/spaces/breezedeus/Pix2Text-Demo)) **to verify the model performance before purchasing**.

**Model Purchase Addresses**:

| Model Name     | Purchase Address                                                       | Description
|--------------|------------------------------------------------------------|-----------------------------------------------------------------------------------
| MFD pro model   | [Lemon Squeezy](https://ocr.lemonsqueezy.com)          | Includes enterprise and personal editions; invoices can be issued. For details, see: [P2T Detailed Information](https://www.breezedeus.com/article/pix2text_cn)    |
| MFD pro model   | [Bilibili](https://mall.bilibili.com/neul-next/detailuniversal/detail.html?isMerchant=1&page=detailuniversal_detail&saleType=10&itemsId=11883911&loadingShow=1&noTitleBar=1&msource=merchant_share) | Includes personal edition only; cannot be used commercially; invoices cannot be issued. For details, see: [P2T Detailed Information](https://www.breezedeus.com/article/pix2text_cn) |
| MFR pro model   | [Lemon Squeezy](https://ocr.lemonsqueezy.com)              | Includes enterprise and personal editions; invoices can be issued. For details, see: [P2T Detailed Information](https://www.breezedeus.com/article/pix2text_cn)    |
| MFR pro model   | [Bilibili](https://mall.bilibili.com/neul-next/detailuniversal/detail.html?isMerchant=1&page=detailuniversal_detail&saleType=10&itemsId=11884166&loadingShow=1&noTitleBar=1&msource=merchant_share)     | Includes personal edition only; cannot be used commercially; invoices cannot be issued. For details, see: [P2T Detailed Information](https://www.breezedeus.com/article/pix2text_cn) |
| CnOCR pro model | [Lemon Squeezy](https://ocr.lemonsqueezy.com)              | Includes enterprise and personal editions; invoices can be issued. For details, see: [P2T Detailed Information](https://www.breezedeus.com/article/pix2text_cn) and [CnOCR Detailed Information](https://www.breezedeus.com/article/cnocr) |
| CnOCR pro model | [Bilibili](https://mall.bilibili.com/neul-next/detailuniversal/detail.html?isMerchant=1&page=detailuniversal_detail&saleType=10&itemsId=11884138&loadingShow=1&noTitleBar=1&msource=merchant_share)     | Includes personal edition only; cannot be used commercially; invoices cannot be issued. For details, see: [P2T Detailed Information](https://www.breezedeus.com/article/pix2text_cn) and [CnOCR Detailed Information](https://www.breezedeus.com/article/cnocr) |

If you encounter problems during the purchase process, you can scan the QR code to add the assistant as a friend for communication. Please note `p2t`, and the assistant will reply as soon as possible:

<figure markdown>
![WeChat Communication Group](https://huggingface.co/datasets/breezedeus/cnocr-wx-qr-code/resolve/main/wx-qr-code.JPG){: style="width:270px"}
</figure>

For more contact information, see [Communication Group](contact.md).
