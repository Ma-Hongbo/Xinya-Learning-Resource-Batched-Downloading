# Gitlab_Batched_Downloader

This repository is a batch downloading program for the Xinya College Learning Resource Library at Tsinghua University.

## For MacOS

Install Python with a version less than or equal to 3.11 and greater than or equal to 3.9.

Git clone this repo.

```bash
cd Gitlab_Batched_Downloader_mac
python3.X -m venv venv
source venv/bin/activate
pip install py2app requests
python3 setup.py py2app
```

## For Windows