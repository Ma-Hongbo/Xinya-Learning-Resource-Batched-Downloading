import os
import json
import threading
import tarfile
from io import BytesIO
import requests
import platform
import subprocess
from parameter import CONFIG_FILE, GITLAB_API

def safe_extractall(tar, path=".", members=None):
    for member in tar.getmembers():
        member_path = os.path.join(path, member.name)
        if not os.path.realpath(member_path).startswith(os.path.realpath(path)):
            raise Exception(f"成员路径 '{member.name}' 存在安全风险，已跳过。")
    tar.extractall(path, members)

def load_token():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f).get("token", "")
        except json.JSONDecodeError:
            return ""
    return ""

def save_token(token):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump({"token": token}, f, ensure_ascii=False, indent=2)

def open_folder(folder_path):
    """✅ 在 Windows 上打开文件夹"""
    if platform.system() == "Windows":
        os.startfile(folder_path)
    elif platform.system() == "Darwin":
        subprocess.call(["open", folder_path])
    else:
        subprocess.call(["xdg-open", folder_path])

def download_repo(token, path, output_dir, log_queue):
    headers = {"PRIVATE-TOKEN": token}
    params = {"path": path}
    log_queue.put("正在下载中，请稍候...\n")

    try:
        response = requests.get(GITLAB_API, headers=headers, params=params, stream=True)
        response.raise_for_status()

        log_queue.put("下载成功，正在解压...\n")
        os.makedirs(output_dir, exist_ok=True)

        with tarfile.open(fileobj=BytesIO(response.content), mode="r:gz") as tar:
            safe_extractall(tar, path=output_dir)

        log_queue.put(f"✅ 解压完成！文件已保存至：{output_dir}\n")
        open_folder(output_dir)
    except Exception as e:
        log_queue.put(f"❌ 下载失败：{e}\n")

def start_download_thread(token, path, output, log_queue):
    thread = threading.Thread(target=download_repo, args=(token, path, output, log_queue), daemon=True)
    thread.start()