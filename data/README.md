# ISIC 2018 Challenge: T1 DataSet




---

## Dataset Overview

Source: https://challenge.isic-archive.com/data/#2018

### Task 1 — Lesion Segmentation

* **Training Data**

  * 2,594 dermoscopic images (10.4 GB)
  * 12,970 segmentation masks (5 per image)

* **Training Ground Truth**

  * 26 MB

* **Validation Data**

  * 228 MB

* **Validation Ground Truth**

  * 742 KB

* **Test Data**

  * 1,000 images (2.2 GB)

* **Test Ground Truth**

  * 9 MB

* **License**

  * **CC-0 (Public Domain)**

---


## Download Instructions

Use one of the provided scripts to download dataset

### Bash

```bash
chmod +x download_dataset.sh
./download.sh
```

### Python

```bash
python3 download_dataset.py
```

---

## Directory Structure

```
data/
├── README.md
├── download_dataset.sh
├── download_dataset.py
├── ISIC2018/
│   ├── training-data/
│   ├── training-ground-truth/
│   ├── validation-data/
│   ├── validation-ground-truth/
│   ├── test-data/
│   └── test-ground-truth/

```


---

## Licensing

This dataset is released under:

* **CC-0 (Public Domain)**


---


