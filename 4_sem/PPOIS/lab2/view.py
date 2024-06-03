import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import List, Optional
from model import Student


class StudentsView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Активисты")
        self.page_size = 10
        self.current_page = 1
        self.total_pages = 1
        self.students: List[Student] = []

        button_frame = ttk.Frame(self)
        button_frame.pack(side=tk.TOP, fill=tk.X)

        self.search_button = tk.Button(button_frame, text="Найти студентов", command=self.open_search_dialog)
        self.search_button.pack(side=tk.LEFT)

        self.add_button = tk.Button(button_frame, text="Добавить студента", command=self.open_add_dialog)
        self.add_button.pack(side=tk.LEFT)

        self.delete_button = tk.Button(button_frame, text="Удалить студентов", command=self.open_delete_dialog)
        self.delete_button.pack(side=tk.LEFT)

        self.load_button = tk.Button(button_frame, text="Загрузить студентов xml", command=self.load_students)
        self.load_button.pack(side=tk.LEFT)

        self.save_button = tk.Button(button_frame, text="Выгрузить студентов xml", command=self.save_students)
        self.save_button.pack(side=tk.LEFT)

        self.show_all_button = tk.Button(button_frame, text="Показать всех студентов", command=self.show_all_students)
        self.show_all_button.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=("fio", "group", "social_work"), show="headings")
        self.tree.heading("fio", text="ФИО")
        self.tree.heading("group", text="Группа")
        self.tree.heading("social_work", text="Общественная работа")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Pagination controls
        pagination_frame = ttk.Frame(self)
        pagination_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.first_page_button = tk.Button(pagination_frame, text="<<", command=self.go_to_first_page)
        self.first_page_button.pack(side=tk.LEFT)

        self.prev_page_button = tk.Button(pagination_frame, text="<", command=self.go_to_prev_page)
        self.prev_page_button.pack(side=tk.LEFT)

        self.page_label = ttk.Label(pagination_frame, text="Страница 1 из 1")
        self.page_label.pack(side=tk.LEFT)

        self.next_page_button = tk.Button(pagination_frame, text=">", command=self.go_to_next_page)
        self.next_page_button.pack(side=tk.LEFT)

        self.last_page_button = tk.Button(pagination_frame, text=">>", command=self.go_to_last_page)
        self.last_page_button.pack(side=tk.LEFT)

        self.page_size_label = ttk.Label(pagination_frame, text="Записей на странице:")
        self.page_size_label.pack(side=tk.LEFT)

        self.page_size_entry = ttk.Entry(pagination_frame, width=5)
        self.page_size_entry.insert(0, "10")
        self.page_size_entry.pack(side=tk.LEFT)
        self.page_size_entry.bind("<Return>", self.update_page_size)

    def set_controller(self, controller):
        self.controller = controller

    def update_students(self, students: List[Student]):
        self.students = students
        self.total_pages = (len(students) + self.page_size - 1) // self.page_size
        self.current_page = 1
        self.update_treeview()

    def update_treeview(self):
        self.tree.delete(*self.tree.get_children())
        start_index = (self.current_page - 1) * self.page_size
        end_index = start_index + self.page_size
        for student in self.students[start_index:end_index]:
            self.tree.insert("", "end", values=(student.fio, student.group, ", ".join(map(str, student.social_work))))
        self.page_label.config(text=f"Страница {self.current_page} из {self.total_pages}")

    def go_to_first_page(self):
        self.current_page = 1
        self.update_treeview()

    def go_to_prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.update_treeview()

    def go_to_next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.update_treeview()

    def go_to_last_page(self):
        self.current_page = self.total_pages
        self.update_treeview()

    def update_page_size(self, event):
        try:
            new_page_size = int(self.page_size_entry.get())
            if new_page_size <= 0:
                raise ValueError
            self.page_size = new_page_size
            self.total_pages = (len(self.students) + self.page_size - 1) // self.page_size
            self.current_page = 1
            self.update_treeview()
        except ValueError:
            self.show_error("Введите положительное целое число.")

    def open_add_dialog(self):
        AddDialog(self)

    def open_search_dialog(self):
        SearchDialog(self, self.controller.get_groups())

    def open_delete_dialog(self):
        DeleteDialog(self, self.controller.get_groups())

    def load_students(self):
        file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
        if file_path:
            self.controller.load_students(file_path)

    def save_students(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML files", "*.xml")])
        if file_path:
            self.controller.save_students(file_path)

    def show_all_students(self):
        self.controller.show_all_students()

    def show_error(self, message: str):
        messagebox.showerror("Error", message)


class AddDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Добавить студента")
        self.geometry("350x300")
        self.parent = parent

        self.fio_label = ttk.Label(self, text="ФИО")
        self.fio_label.pack()
        self.fio_entry = ttk.Entry(self, width=30)
        self.fio_entry.pack()

        self.group_label = ttk.Label(self, text="Группа")
        self.group_label.pack()
        self.group_entry = ttk.Entry(self, width=10)
        self.group_entry.pack()

        self.social_work_label = ttk.Label(self, text="Общественная работа (10 целых чисел через запятую)")
        self.social_work_label.pack()
        self.social_work_entry = ttk.Entry(self, width=30)
        self.social_work_entry.pack()

        self.add_button = ttk.Button(self, text="Добавить", command=self.add_student)
        self.add_button.pack()

    def add_student(self):
        fio = self.fio_entry.get()
        group = self.group_entry.get()
        try:
            social_work = list(map(int, self.social_work_entry.get().split(',')))
            if len(social_work) != 10:
                raise ValueError("Введите ровно 10 чисел.")
            student = Student(fio=fio, group=group, social_work=social_work)
            self.parent.controller.add_student(student)
            self.destroy()
        except ValueError as e:
            self.parent.show_error(f"Неправильный ввод: {e}")


class SearchDialog(tk.Toplevel):
    def __init__(self, parent, groups: List[str]):
        super().__init__(parent)
        self.title("Поиск студентов")
        self.geometry("400x500")
        self.parent = parent

        self.search_by_label = ttk.Label(self, text="Искать по:")
        self.search_by_label.pack()

        self.search_options = ttk.Combobox(self, values=["Фамилия", "Группа", "Фамилия и работа", "Группа и работа"])
        self.search_options.pack()
        self.search_options.bind("<<ComboboxSelected>>", self.show_fields)

        self.group_var = tk.StringVar()
        self.group_combo = ttk.Combobox(self, textvariable=self.group_var, values=groups)
        self.group_combo.pack()
        self.group_combo.pack_forget()

        self.fio_entry = ttk.Entry(self, width=30)
        self.fio_entry.pack()
        self.fio_entry.pack_forget()

        self.work_min_label = ttk.Label(self, text="Минимальная оценка за работу")
        self.work_min_label.pack_forget()
        self.work_min_entry = ttk.Entry(self)
        self.work_min_entry.pack_forget()

        self.work_max_label = ttk.Label(self, text="Максимальная оценка за работу")
        self.work_max_label.pack_forget()
        self.work_max_entry = ttk.Entry(self)
        self.work_max_entry.pack_forget()

        self.search_button = ttk.Button(self, text="Поиск", command=self.search_students)
        self.search_button.pack()

        self.result_label = ttk.Label(self, text="")

    def show_fields(self, event):
        option = self.search_options.get()
        self.group_combo.pack_forget()
        self.fio_entry.pack_forget()
        self.work_min_label.pack_forget()
        self.work_min_entry.pack_forget()
        self.work_max_label.pack_forget()
        self.work_max_entry.pack_forget()
        self.result_label.pack_forget()

        if option == "Фамилия":
            self.fio_entry.pack()
        elif option == "Группа":
            self.group_combo.pack()
        elif option == "Фамилия и работа":
            self.fio_entry.pack()
            self.work_min_label.pack()
            self.work_min_entry.pack()
            self.work_max_label.pack()
            self.work_max_entry.pack()
        elif option == "Группа и работа":
            self.group_combo.pack()
            self.work_min_label.pack()
            self.work_min_entry.pack()
            self.work_max_label.pack()
            self.work_max_entry.pack()

    def search_students(self):
        option = self.search_options.get()
        work_min = self.work_min_entry.get()
        work_max = self.work_max_entry.get()

        work_min = int(work_min) if work_min else None
        work_max = int(work_max) if work_max else None

        if option == "Фамилия":
            fio = self.fio_entry.get()
            results = self.parent.controller.search_students(fio=fio, work_min=work_min, work_max=work_max)
        elif option == "Группа":
            group = self.group_var.get()
            results = self.parent.controller.search_students(group=group, work_min=work_min, work_max=work_max)
        elif option == "Фамилия и работа":
            fio = self.fio_entry.get()
            results = self.parent.controller.search_students(fio=fio, work_min=work_min, work_max=work_max)
        elif option == "Группа и работа":
            group = self.group_var.get()
            results = self.parent.controller.search_students(group=group, work_min=work_min, work_max=work_max)

        self.display_results(results)

    def display_results(self, results):
        result_text = "\n".join([f"{student.fio},  {student.group},  {student.social_work}" for student in results])
        self.result_label.config(text=("Результаты поиска:\n" + result_text))
        self.result_label.pack()


class DeleteDialog(tk.Toplevel):
    def __init__(self, parent, groups: List[str]):
        super().__init__(parent)
        self.title("Удалить студентов")
        self.geometry("300x200")
        self.parent = parent

        self.delete_by_label = ttk.Label(self, text="Удалить по:")
        self.delete_by_label.pack()

        self.delete_options = ttk.Combobox(self, values=["Фамилия", "Группа", "Фамилия и работа", "Группа и работа"])
        self.delete_options.pack()
        self.delete_options.bind("<<ComboboxSelected>>", self.show_fields)

        self.group_var = tk.StringVar()
        self.group_combo = ttk.Combobox(self, textvariable=self.group_var, values=groups)
        self.group_combo.pack()
        self.group_combo.pack_forget()

        self.fio_entry = ttk.Entry(self, width=30)
        self.fio_entry.pack()
        self.fio_entry.pack_forget()

        self.work_min_label = ttk.Label(self, text="Минимальная оценка за работу")
        self.work_min_label.pack_forget()
        self.work_min_entry = ttk.Entry(self)
        self.work_min_entry.pack_forget()

        self.work_max_label = ttk.Label(self, text="Максимальная оценка за работу")
        self.work_max_label.pack_forget()
        self.work_max_entry = ttk.Entry(self)
        self.work_max_entry.pack_forget()

        self.delete_button = ttk.Button(self, text="Удалить", command=self.delete_students)
        self.delete_button.pack()

        self.result_label = ttk.Label(self, text="")
        self.result_label.pack_forget()

    def show_fields(self, event):
        option = self.delete_options.get()
        self.group_combo.pack_forget()
        self.fio_entry.pack_forget()
        self.work_min_label.pack_forget()
        self.work_min_entry.pack_forget()
        self.work_max_label.pack_forget()
        self.work_max_entry.pack_forget()
        self.result_label.pack_forget()

        if option == "Фамилия":
            self.fio_entry.pack()
        elif option == "Группа":
            self.group_combo.pack()
        elif option == "Фамилия и работа":
            self.fio_entry.pack()
            self.work_min_label.pack()
            self.work_min_entry.pack()
            self.work_max_label.pack()
            self.work_max_entry.pack()
        elif option == "Группа и работа":
            self.group_combo.pack()
            self.work_min_label.pack()
            self.work_min_entry.pack()
            self.work_max_label.pack()
            self.work_max_entry.pack()

    def delete_students(self):
        option = self.delete_options.get()
        work_min = self.work_min_entry.get()
        work_max = self.work_max_entry.get()

        work_min = int(work_min) if work_min else None
        work_max = int(work_max) if work_max else None

        if option == "Фамилия":
            fio = self.fio_entry.get()
            deleted_count = self.parent.controller.delete_students(fio=fio, work_min=work_min, work_max=work_max)
        elif option == "Группа":
            group = self.group_var.get()
            deleted_count = self.parent.controller.delete_students(group=group, work_min=work_min, work_max=work_max)
        elif option == "Фамилия и работа":
            fio = self.fio_entry.get()
            deleted_count = self.parent.controller.delete_students(fio=fio, work_min=work_min, work_max=work_max)
        elif option == "Группа и работа":
            group = self.group_var.get()
            deleted_count = self.parent.controller.delete_students(group=group, work_min=work_min, work_max=work_max)

        self.display_results(deleted_count)

    def display_results(self, deleted_count):
        self.result_label.config(text=f"Удалено студентов: {deleted_count}")
        self.result_label.pack()

