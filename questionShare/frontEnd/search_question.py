import tkinter as tk
from tkinter import messagebox
import os
from question import EssayQuestion, MultipleChoiceQuestion

# 文件路径
FILE_PATH = "file0/"

# 搜索问题
def search_question():
    root = tk.Tk()
    root.title("搜索问题")

    # 创建搜索问题界面
    search_frame = tk.Frame(root)
    search_frame.pack(pady=20)

    tk.Label(search_frame, text="问题名称:").grid(row=0, column=0)
    question_entry = tk.Entry(search_frame)
    question_entry.grid(row=0, column=1)

    def search():
        question_name = question_entry.get()
        if not question_name:
            messagebox.showwarning("搜索问题", "请输入问题名称！")
            return

        # 执行搜索问题的功能
        matched_questions = search_matched_questions(question_name)
        display_matched_questions(matched_questions)

    def search_matched_questions(question_name):
        file_path = os.path.join(FILE_PATH, "questions.txt")
        with open(file_path, "r") as file:
            questions = file.readlines()

        matched_questions = []
        for question in questions:
            question = question.strip().split(",")
            if question_name.lower() in question[0].lower():
                if question[3] == "essay":
                    matched_questions.append(EssayQuestion(question[0], question[1], question[2]))
                else:
                    options = question[1:5]
                    matched_questions.append(MultipleChoiceQuestion(question[0], options, question[5]))

        return matched_questions

    def display_matched_questions(matched_questions):
        display_window = tk.Toplevel(root)
        display_window.title("搜索结果")

        text_box = tk.Text(display_window, height=10, width=50)
        text_box.pack(pady=20)

        if matched_questions:
            for question in matched_questions:
                text_box.insert(tk.END, f"问题名称: {question.question_name}\n")
                if isinstance(question, EssayQuestion):
                    text_box.insert(tk.END, f"问题类型: 简答题\n")
                    text_box.insert(tk.END, f"答案: {question.question_answer}\n")
                elif isinstance(question, MultipleChoiceQuestion):
                    text_box.insert(tk.END, f"问题类型: 选择题\n")
                    text_box.insert(tk.END, f"选项: {' ;'.join([chr(ord('A')+i) + ': ' + opt for i, opt in enumerate(question.options)])}\n")
                text_box.insert(tk.END, f"问题组名称: {question.question_group}\n")
                text_box.insert(tk.END, "\n")
        else:
            text_box.insert(tk.END, "未找到匹配的问题")

        text_box.config(state=tk.DISABLED)

    tk.Button(search_frame, text="搜索", command=search).grid(row=1, column=0, columnspan=2)

    root.mainloop()
