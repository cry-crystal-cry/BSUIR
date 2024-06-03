from typing import List, Optional
from model import Student, StudentsModel
from view import StudentsView


class StudentsController:
    def __init__(self, model: StudentsModel, view: StudentsView):
        self.model = model
        self.view = view
        self.view.set_controller(self)

    def load_students(self, file_path: str):
        try:
            self.model.load_students(file_path)
            self.view.update_students(self.model.students)
        except Exception as e:
            self.view.show_error(f"Ошибка загрузки xml: {e}")

    def save_students(self, file_path: str):
        try:
            self.model.save_students(file_path)
        except Exception as e:
            self.view.show_error(f"Ошибка выгрузки xml: {e}")

    def add_student(self, student: Student):
        try:
            self.model.add_student(student)
            self.view.update_students(self.model.students)
        except Exception as e:
            self.view.show_error(f"Ошибка при добавлении студента: {e}")

    def delete_students(self, fio: Optional[str] = None, group: Optional[str] = None, work_min: Optional[int] = None,
                        work_max: Optional[int] = None) -> int:
        try:
            deleted_count = self.model.delete_students(fio, group, work_min, work_max)
            self.view.update_students(self.model.students)
            return deleted_count
        except Exception as e:
            self.view.show_error(f"Ошибка при удалении студентов: {e}")
            return 0

    def search_students(self, fio: Optional[str] = None, group: Optional[str] = None, work_min: Optional[int] = None,
                        work_max: Optional[int] = None) -> List[Student]:
        try:
            results = self.model.search_students(fio, group, work_min, work_max)
            self.view.update_students(results)
            return results
        except Exception as e:
            self.view.show_error(f"Ошибка при поиске студентов: {e}")
            return []

    def show_all_students(self):
        try:
            self.view.update_students(self.model.students)
        except Exception as e:
            self.view.show_error(f"Ошибка отображения всех студентов: {e}")

    def get_groups(self) -> List[str]:
        return self.model.get_groups()

    def start(self):
        self.view.mainloop()


if __name__ == "__main__":
    model = StudentsModel()
    view = StudentsView()
    controller = StudentsController(model, view)
    controller.start()
