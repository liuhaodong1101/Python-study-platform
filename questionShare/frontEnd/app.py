import tkinter as tk
from tkinter import messagebox
from tkinter import Menu
import os
from upload_question import upload_question
from search_question import search_question
from search_group import search_group

class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.FILE_PATH = "file0/"
        self.create_widgets()

    def create_widgets(self):
        self.master.title("问题管理系统")
        self.menubar = Menu(self.master)
        self.master.config(menu=self.menubar)
        self.question_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="问题", menu=self.question_menu)
        self.question_menu.add_command(label="上传问题", command=self.upload_question)
        self.question_menu.add_command(label="搜索问题", command=self.search_question)
        self.question_menu.add_command(label="搜索问题组", command=self.search_group)

        self.solve_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="解题", menu=self.solve_menu)
        self.solve_menu.add_command(label="解题功能", command=self.solve_question)

        # 创建个人信息菜单
        info_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="个人信息", menu=info_menu)
        info_menu.add_command(label="查看账号密码", command=self.view_account_info)
        info_menu.add_command(label="修改密码", command=self.change_password)

        # 加入组
        info_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="查看小组", menu=info_menu)
        info_menu.add_command(label="查看当前小组", command=self.chekck_cur_group)
        info_menu.add_command(label="加入小组", command=self.join_a_group)

    def run(self):
        self.master.mainloop()

    # 查看账号密码功能
    def view_account_info(self):
        messagebox.showinfo("个人信息", "账号：user123\n密码：********")

    # 修改密码功能
    def change_password(self):
        messagebox.showinfo("修改密码", "请输入新密码。")


    def upload_question(self):
        upload_question()

    def search_question(self):
        search_question()

    def search_group(self):
        search_group()

    def solve_question(self):
        root_solve = tk.Toplevel(self.master)
        root_solve.title("解题")

        solve_frame = tk.Frame(root_solve)
        solve_frame.pack(pady=20)

        tk.Label(solve_frame, text="可选题目:").grid(row=0, column=0)

        questions = self.get_questions_list()
        question_listbox = tk.Listbox(solve_frame, width=50)
        question_listbox.grid(row=1, column=0)

        for question in questions:
            question_listbox.insert(tk.END, question)

        def show_question_details():
            selected_question = question_listbox.get(tk.ACTIVE)
            question_details_frame = tk.Frame(solve_frame)
            question_details_frame.grid(row=2, column=0, pady=10)

            question_details = self.get_question_details(selected_question)

            if question_details:
                question_type = question_details[0]
                if question_type == "essay":
                    tk.Label(question_details_frame, text="问题类型: 简答题").pack()
                    tk.Label(question_details_frame, text="问题答案:").pack()
                    answer_entry = tk.Entry(question_details_frame)
                    answer_entry.pack()
                else:
                    tk.Label(question_details_frame, text="问题类型: 选择题").pack()
                    tk.Label(question_details_frame, text="问题选项:").pack()
                    options = question_details[1:]
                    for i, option in enumerate(options):
                        tk.Label(question_details_frame, text=f"{chr(ord('A')+i)}. {option}").pack()
                    tk.Label(question_details_frame, text="请选择答案:").pack()
                    answer_entry = tk.Entry(question_details_frame)
                    answer_entry.pack()

                def submit_answer():
                    answer = answer_entry.get()
                    messagebox.showinfo("提交答案", f"您的答案是：{answer}")

                submit_button = tk.Button(question_details_frame, text="提交答案", command=submit_answer)
                submit_button.pack(pady=10)
            else:
                tk.Label(question_details_frame, text="未找到问题的详细信息").pack()

        solve_button = tk.Button(solve_frame, text="解题", command=show_question_details)
        solve_button.grid(row=3, column=0, pady=10)

    def get_questions_list(self):
        file_path = os.path.join(self.FILE_PATH, "questions.txt")
        with open(file_path, "r") as file:
            lines = file.readlines()

        questions = [line.split(",")[0] for line in lines]
        return questions

    def get_question_details(self, question_name):
        file_path = os.path.join(self.FILE_PATH, "questions.txt")
        with open(file_path, "r") as file:
            lines = file.readlines()

        for line in lines:
            line = line.strip().split(",")
            if line[0] == question_name:
                return line[3:]

        return []

    def chekck_cur_group(self):
        root = tk.Tk()
        root.title("当前小组")
        search_frame = tk.Frame(root)
        search_frame.pack(pady=20)
        tk.Label(search_frame, text="你当前的小组为:").grid(row=0, column=0)

    def join_a_group(self):
        root = tk.Tk()
        root.title("当前小组")
        search_frame = tk.Frame(root)
        search_frame.pack(pady=20)
    # tk.Listbox(search_frame, text="当前的小组有:").grid(row=0, column=0)

