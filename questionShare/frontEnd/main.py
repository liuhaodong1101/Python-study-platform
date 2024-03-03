import tkinter as tk
from login import LoginApp

# 创建主窗口
root = tk.Tk()
root.title("应用程序")

# 创建登录应用程序实例
login_app = LoginApp(root)

# 显示登录应用程序界面
login_app.login_frame.pack()

root.mainloop()
