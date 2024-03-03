import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import os
from question import EssayQuestion, MultipleChoiceQuestion

# 文件路径
FILE_PATH = "file0/"

# 上传问题
def upload_question():
    root = tk.Tk()
    root.title("上传问题")

    # 创建上传问题界面
    upload_frame = tk.Frame(root)
    upload_frame.pack(pady=20)

    tk.Label(upload_frame, text="问题描述:").grid(row=0, column=0)
    question_entry = tk.Entry(upload_frame)
    question_entry.grid(row=0, column=1)

    tk.Label(upload_frame, text="问题组名称:").grid(row=1, column=0)
    group_entry = tk.Entry(upload_frame)
    group_entry.grid(row=1, column=1)

    question_type = tk.IntVar()
    question_type.set(0)
    def set2(self):
        self.set(2)
    tk.Label(upload_frame, text="问题类型:").grid(row=2, column=0)
    tk.Radiobutton(upload_frame, text="简答题", variable=question_type, value=1).grid(row=2, column=1, sticky="w")
    tk.Radiobutton(upload_frame, text="选择题", variable=question_type, value=2,command=set2(question_type)).grid(row=2, column=1, sticky="e")

    def upload():
        question_name = question_entry.get()
        question_group = group_entry.get()

        if not question_name or not question_group:
            messagebox.showwarning("上传问题", "请填写完整的问题信息！")
            return
        question_type_value = question_type.get()
        if question_type_value == 1:
            question_answer = simpledialog.askstring("上传问题", "请输入简答题答案：")
            if not question_answer:
                messagebox.showwarning("上传问题", "请输入简答题答案！")
                return

            question = EssayQuestion(question_name, question_answer, question_group)
        elif question_type_value == 2:
            options = []
            for i in range(1, 5):
                option = simpledialog.askstring("上传问题", f"请输入第{i}个选项：")
                if not option:
                    messagebox.showwarning("上传问题", f"请输入第{i}个选项！")
                    return
                options.append(option)

            question = MultipleChoiceQuestion(question_name, options, question_group)
        else:
            print(question_type.get())
            print("aaa")
            messagebox.showwarning("上传问题", "无效的问题类型！")
            return

        # 将问题信息保存到文件
        file_path = os.path.join(FILE_PATH, "questions.txt")
        with open(file_path, "a") as file:
            if isinstance(question, EssayQuestion):
                file.write(f"{question.question_name},{question.question_answer},{question.question_group},essay\n")
            elif isinstance(question, MultipleChoiceQuestion):
                options = ",".join(question.options)
                file.write(f"{question.question_name},{options},{question.question_group},multiple_choice\n")

        messagebox.showinfo("问题上传成功", "问题上传成功！")

    def browse_file():
        file_path = filedialog.askopenfilename(initialdir=".", title="选择问题文件")
        if file_path:
            process_file(file_path)

    def process_file(file_path):
        with open(file_path, "r") as file:
            lines = file.readlines()

        for line in lines:
            line = line.strip()
            if line:
                upload_single_question(line)

        messagebox.showinfo("问题上传成功", "问题上传成功！")

    def upload_single_question(line):
        question_info = line.split(",")
        question_type = question_info[3]

        if question_type == "essay":
            question_name = question_info[0]
            options = question_info[1]
            question_group = question_info[2]
            question = EssayQuestion(question_name, options[0], question_group)
        elif question_info[6] == "multiple_choice":
            question_name = question_info[0]
            options = question_info[1:5]
            question_group = question_info[5]
            question = MultipleChoiceQuestion(question_name, options, question_group)
        else:
            messagebox.showwarning("上传问题", f"无效的问题类型：{question_type}")
            return

        # 将问题信息保存到文件
        file_path = os.path.join(FILE_PATH, "questions.txt")
        with open(file_path, "a") as file:
            if isinstance(question, EssayQuestion):
                file.write(f"{question.question_name},{question.question_answer},{question.question_group},essay\n")
            elif isinstance(question, MultipleChoiceQuestion):
                options = ",".join(question.options)
                file.write(f"{question.question_name},{options},{question.question_group},multiple_choice\n")

    tk.Button(upload_frame, text="上传", command=upload).grid(row=3, column=0, columnspan=2)
    tk.Button(upload_frame, text="浏览文件", command=browse_file).grid(row=4, column=0, columnspan=2)

    root.mainloop()
