from tkinter import ttk
from utils import save_token

class TokenPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, pady=20)

        ttk.Label(frame, text="GitLab Token:", font=("Arial", 12)).pack(pady=10)
        ttk.Entry(frame, textvariable=controller.token_var, width=50).pack(pady=5)

        ttk.Button(frame, text="保存Token", command=lambda: [save_token(controller.token_var.get()), controller.log("✅ Token 已保存！\n")]).pack(pady=10)