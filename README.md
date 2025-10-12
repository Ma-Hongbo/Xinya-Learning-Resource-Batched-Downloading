# **GitLab Batched Downloader**

This repository provides a **batch downloading utility** for the **Xinya College Learning Resource Library** at **Tsinghua University**.
It supports both **macOS** and **Windows**, allowing users to securely and conveniently download specific directories from the Tsinghua GitLab repository.

---

## Features

* 🔒 Secure access using your **private GitLab token**
* 📦 Automatically **downloads and extracts** repository archives
* ⚙️ Supports both **macOS app packaging** and **Windows executable builds**
---

## 🍎 macOS Installation & Usage

### 1. Environment Setup

Make sure you have **Python 3.11** installed.

Clone this repository:

```bash
git clone git@github.com:Ma-Hongbo/Xinya-Learning-Resource-Batched-Downloading.git
cd ~/Gitlab_Batched_Downloader_mac
```

Create and activate a virtual environment:

```bash
python3.11 -m venv venv
source venv/bin/activate
```

Install dependencies and build the macOS app:

```bash
pip install py2app requests
python3 setup.py py2app
```

After building, you can find the executable app at:

```
~/Gitlab_Batched_Downloader_mac/dist
```

### 2. Debug Mode

You can run the app directly from the build directory for debugging:

```bash
cd ～/Gitlab_Batched_Downloader_mac
dist/GitRepoDownloader.app/Contents/MacOS/GitRepoDownloader
```

---

## 🪟 Windows Installation & Usage

### 1. Environment Setup

Ensure you are using **Windows** and have **Anaconda** or **Miniconda** installed.

Create and activate a virtual environment:

```bash
cd ～/Gitlab_Batched_Downloader_win
conda create -n Gitlab_Batched_Downloader python=3.11
conda activate Gitlab_Batched_Downloader
```

### 2. Build Executable

Install required dependencies and package the project with **PyInstaller**:

```bash
pip install pyinstaller requests
pyinstaller --noconsole --onefile main.py
```

After building, the executable can be found at:

```
~/Gitlab_Batched_Downloader_win/dist
```

---

## 📄 License

This project is developed for **educational use** within Tsinghua University.
Please contact the maintainer before redistributing or modifying it for other purposes.
