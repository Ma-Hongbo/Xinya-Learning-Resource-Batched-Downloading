import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
from utils import start_download_thread

class MainPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        content_frame = ttk.Frame(self)
        content_frame.pack(fill="both", expand=True)

        ttk.Label(content_frame, text="下载路径 (GitLab 仓库内路径):").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(content_frame, textvariable=controller.path_var, width=50).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)

        ttk.Label(content_frame, text="保存路径:").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(content_frame, textvariable=controller.output_var, width=50).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2)
        ttk.Button(content_frame, text="选择...", command=self.browse_folder).grid(row=1, column=2, padx=(5, 0), pady=2)

        ttk.Button(content_frame, text="开始下载", command=self.start_download_action).grid(row=2, column=0, columnspan=3, pady=10)

        self.log_text = scrolledtext.ScrolledText(content_frame, wrap=tk.WORD, height=10, state="disabled")
        self.log_text.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(5, 0))

        content_frame.columnconfigure(1, weight=1)
        content_frame.rowconfigure(3, weight=1)
        
    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.controller.output_var.set(folder_selected)
            
    def start_download_action(self):
        token = self.controller.token_var.get()
        path = self.controller.path_var.get()
        output = self.controller.output_var.get()

        if not token:
            self.controller.log("❌ 请先输入并保存Token!\n")
            return
        if not path:
            self.controller.log("❌ 请输入下载路径(path)!\n")
            return
        if not output:
            self.controller.log("❌ 请选择输出文件夹!\n")
            return
        
        start_download_thread(token, path, output, self.controller.log_queue)