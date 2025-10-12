import os
import platform

import tkinter as tk
from tkinter import ttk
import queue

from pages.mainpage import MainPage
from pages.tokenpage import TokenPage
from pages.contactpage import ContactPage
from utils import load_token



class App:
    def __init__(self, root):
        self.root = root
        self.root.title("新雅书院学习资料库下载器")
        self.root.geometry("670x300")
        
        if platform.system() == "Windows":
            default_font = ("Microsoft YaHei UI", 10)
        else:
            default_font = ("Arial", 11)
        self.root.option_add("*Font", default_font)

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

        self.top_frame = ttk.Frame(self.root)
        self.top_frame.pack(side="top", fill="x", padx=5, pady=5)
        ttk.Button(self.top_frame, text="主界面", command=lambda: self.show_frame(MainPage)).pack(side="left", padx=5)
        ttk.Button(self.top_frame, text="Token设置", command=lambda: self.show_frame(TokenPage)).pack(side="left", padx=5)
        ttk.Button(self.top_frame, text="联系我们", command=lambda: self.show_frame(ContactPage)).pack(side="left", padx=5)
        self.container = ttk.Frame(self.root)
        self.container.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.frames = {}
        for F in (MainPage, TokenPage, ContactPage):
            frame = F(parent=self.container, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainPage)
        self.process_log_queue()

    def show_frame(self, page_class):
        frame = self.frames[page_class]
        frame.tkraise()

    def log(self, message):
        self.frames[MainPage].log_text.config(state="normal")
        self.frames[MainPage].log_text.insert(tk.END, message)
        self.frames[MainPage].log_text.config(state="disabled")
        self.frames[MainPage].log_text.see(tk.END)

    def process_log_queue(self):
        try:
            message = self.log_queue.get_nowait()
            self.log(message)
        except queue.Empty:
            pass
        self.root.after(100, self.process_log_queue)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
