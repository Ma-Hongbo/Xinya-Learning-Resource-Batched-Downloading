import tkinter as tk
from tkinter import ttk

class ContactPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, pady=20)

        contact_info = (
            "本项目由马洪博(新雅21),刘炳麟(新雅31)及新雅学社学习部创建并开发\n\n"
            "如你在使用中遇到了问题,或是对此有改进建议,抑或是想一起对此进行维护\n"
            "欢迎联系我们！\n\n"
            "邮箱: mahb22@mails.tsinghua.edu.cn\n"
            "微信: 可在新雅大群中添加\n\n"
            "本项目已经在GitHub开源,\n"
            "欢迎访问:https://github.com/Ma-Hongbo/Xinya-Learning-Resource-Batched-Downloading\n\n"
            "感谢使用！"
        )
        ttk.Label(frame, text=contact_info, justify=tk.LEFT, wraplength=600).pack(padx=10, pady=10)