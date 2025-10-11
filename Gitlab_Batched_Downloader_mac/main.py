import os
import json
import threading
import tarfile
from io import BytesIO
import requests

import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import queue

CONFIG_FILE = "token.json"
GITLAB_API = "https://git.tsinghua.edu.cn/api/v4/projects/38341/repository/archive.tar.gz"

def load_token():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f).get("token", "")
        except json.JSONDecodeError:
            return ""
    return ""

def save_token(token):
    with open(CONFIG_FILE, "w") as f:
        json.dump({"token": token}, f)

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

# -------------------- 多页面应用 --------------------
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("新雅书院学习资料库下载器")
        self.root.geometry("600x400")

        icon_path = "icon.png"
        if os.path.exists(icon_path):
            try:
                self.root.iconphoto(True, tk.PhotoImage(file=icon_path))
            except Exception as e:
                print(f"设置图标失败: {e}")

        self.style = ttk.Style(self.root)
        self.style.theme_use("clam")

        self.token_var = tk.StringVar(value=load_token())
        self.path_var = tk.StringVar()
        self.output_var = tk.StringVar()
        self.log_queue = queue.Queue()

        # 顶部菜单栏
        self.top_frame = ttk.Frame(self.root)
        self.top_frame.pack(side="top", fill="x", padx=5, pady=5)
        ttk.Button(self.top_frame, text="主界面", command=lambda: self.show_frame(MainPage)).pack(side="left", padx=5)
        ttk.Button(self.top_frame, text="Token设置", command=lambda: self.show_frame(TokenPage)).pack(side="left", padx=5)
        ttk.Button(self.top_frame, text="联系我们", command=lambda: self.show_frame(ContactPage)).pack(side="left", padx=5)

        # 页面容器
        self.container = ttk.Frame(self.root)
        self.container.pack(fill="both", expand=True, padx=10, pady=(0,10))

        # 创建所有页面
        self.frames = {}
        for F in (MainPage, TokenPage, ContactPage):
            frame = F(parent=self.container, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # 显示主界面
        self.show_frame(MainPage)
        self.process_log_queue()

    def show_frame(self, page_class):
        frame = self.frames[page_class]
        frame.tkraise()

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.output_var.set(folder_selected)

    def start_download_action(self):
        token = self.token_var.get()
        path = self.path_var.get()
        output = self.output_var.get()

        if not token:
            self.log("❌ 请先输入并保存Token!\n")
            return
        if not path:
            self.log("❌ 请输入下载路径(path)!\n")
            return
        if not output:
            self.log("❌ 请选择输出文件夹!\n")
            return
        
        start_download_thread(token, path, output, self.log_queue)

    def log(self, message):
        self.frames[MainPage].log_text.config(state='normal')
        self.frames[MainPage].log_text.insert(tk.END, message)
        self.frames[MainPage].log_text.config(state='disabled')
        self.frames[MainPage].log_text.see(tk.END)

    def process_log_queue(self):
        try:
            message = self.log_queue.get_nowait()
            self.log(message)
        except queue.Empty:
            pass
        self.root.after(100, self.process_log_queue)

# -------------------- 页面：主界面 --------------------
class MainPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        content_frame = ttk.Frame(self)
        content_frame.pack(fill="both", expand=True)

        ttk.Label(content_frame, text="下载路径:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(content_frame, textvariable=controller.path_var, width=50).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)

        ttk.Label(content_frame, text="保存路径:").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(content_frame, textvariable=controller.output_var, width=50).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2)
        ttk.Button(content_frame, text="选择...", command=controller.browse_folder).grid(row=1, column=2, padx=(5,0), pady=2)

        ttk.Button(content_frame, text="开始下载", command=controller.start_download_action).grid(row=2, column=0, columnspan=3, pady=10)

        self.log_text = scrolledtext.ScrolledText(content_frame, wrap=tk.WORD, height=10, state='disabled')
        self.log_text.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(5,0))

        content_frame.columnconfigure(1, weight=1)
        content_frame.rowconfigure(3, weight=1)

# -------------------- 页面：Token设置 --------------------
class TokenPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, pady=20)

        ttk.Label(frame, text="GitLab Token:", font=("Arial", 12)).pack(pady=10)
        ttk.Entry(frame, textvariable=controller.token_var, width=50).pack(pady=5)

        ttk.Button(frame, text="保存Token", command=lambda: [save_token(controller.token_var.get()), controller.log("✅ Token 已保存！\n")]).pack(pady=10)

# -------------------- 页面：联系我们 --------------------
class ContactPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, pady=20)

        contact_info = (
            "本项目由马洪博(新雅21),刘炳麟(新雅31)创建并开发\n\n"
            "如在使用中遇到了问题,或是对此有改进建议,或是想一起对此进行维护\n"
            "欢迎联系我们！\n\n"
            "邮箱: mahb22@mails.tsinghua.edu.cn\n"
            "微信: 可在新雅大群中添加\n\n"
            "本项目已经在GitHub开源,欢迎访问:\n"
            "感谢使用！"
        )
        ttk.Label(frame, text=contact_info, justify=tk.LEFT, font=("Arial", 11)).pack(padx=10, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
