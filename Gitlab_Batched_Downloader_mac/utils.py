import os
import json
import threading
import tarfile
from io import BytesIO
import requests

from parameter import CONFIG_FILE, GITLAB_API



def save_token(token):
    with open(CONFIG_FILE, "w") as f:
        json.dump({"token": token}, f)
        
def load_token():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f).get("token", "")
        except json.JSONDecodeError:
            return ""
    return ""

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
            for member in tar.getmembers():
                member_path = os.path.join(output_dir, member.name)
                if not os.path.realpath(member_path).startswith(os.path.realpath(output_dir)):
                     raise Exception(f"成员路径 '{member.name}' 存在安全风险，已跳过。")
            tar.extractall(path=output_dir)

        log_queue.put(f"解压完成！文件已保存至：{output_dir}\n")
    except Exception as e:
        log_queue.put(f"下载失败：{e}\n")

def start_download_thread(token, path, output, log_queue):
    thread = threading.Thread(target=download_repo, args=(token, path, output, log_queue), daemon=True)
    thread.start()