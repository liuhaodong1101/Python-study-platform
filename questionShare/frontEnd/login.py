import tkinter as tk
from tkinter import messagebox
import os
from app import App

# 文件路径
FILE_PATH = "file0/"

# 登录应用程序
class LoginApp:
    def __init__(self, root):
        self.root = root

        # 用户登录界面
        self.login_frame = tk.Frame(root)
        self.login_frame.pack(pady=20)

        tk.Label(self.login_frame, text="用户名:").grid(row=0, column=0)
        self.login_username_entry = tk.Entry(self.login_frame)
        self.login_username_entry.grid(row=0, column=1)

        tk.Label(self.login_frame, text="密码:").grid(row=1, column=0)
        self.login_password_entry = tk.Entry(self.login_frame, show="*")
        self.login_password_entry.grid(row=1, column=1)

        tk.Button(self.login_frame, text="登录", command=self.login).grid(row=2, column=0)
        tk.Button(self.login_frame, text="注册", command=self.register).grid(row=2, column=1)

    def login(self):
        username = self.login_username_entry.get()
        password = self.login_password_entry.get()

        # 从文件中验证用户名和密码
        file_path = os.path.join(FILE_PATH, "users.txt")
        with open(file_path, "r") as file:
            lines = file.readlines()
            for line in lines:
                user_info = line.strip().split(",")
                if user_info[0] == username and user_info[1] == password:
                    messagebox.showinfo("登录成功", "用户登录成功！")
                    self.root.destroy()
                    self.open_app()
                    return

        messagebox.showerror("登录失败", "用户名或密码错误！")

    def register(self):
        username = self.login_username_entry.get()
        password = self.login_password_entry.get()

        # 验证用户名是否已存在
        file_path = os.path.join(FILE_PATH, "users.txt")
        with open(file_path, "r") as file:
            lines = file.readlines()
            for line in lines:
                user_info = line.strip().split(",")
                if user_info[0] == username:
                    messagebox.showerror("注册失败", "用户名已存在！")
                    return

        # 将用户信息保存到文件
        with open(file_path, "a") as file:
            file.write(f"{username},{password}\n")

        messagebox.showinfo("注册成功", "用户注册成功！")

    def open_app(self):
        # 创建主窗口
        root = tk.Tk()
        root.title("应用程序")

        # 创建应用程序实例
        app = App(root)

        # 显示应用程序界面
        app.pack()

        root.mainloop()
