import os 

def get_config_path():
    app_dir = ""
    if os.name == "nt":  # Windows
        app_dir = os.path.join(os.getenv("APPDATA"), "GitDownloader")
    else:  # macOS / Linux
        app_dir = os.path.join(os.path.expanduser("~"), ".git_downloader")
    os.makedirs(app_dir, exist_ok=True)
    return os.path.join(app_dir, "token.json")

CONFIG_FILE = get_config_path()

GITLAB_API = "https://git.tsinghua.edu.cn/api/v4/projects/38341/repository/archive.tar.gz"