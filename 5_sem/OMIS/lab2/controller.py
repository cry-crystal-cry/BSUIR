from db import init_db, print_db_info
from model import TaskService, TaskRepository, AuthService, UserRepository, MaterialService, MaterialRepository, ProgressService, ProgressRepository, FeedbackService, FeedbackRepository
from view import TaskView, AuthView, MaterialView, ProgressView, FeedbackView

# Инициализация базы данных
init_db()

# Вывод информации о базе данных
print_db_info()

# Контроллеры
class TaskController:
    def __init__(self):
        self.task_service = TaskService(TaskRepository())
        self.task_view = TaskView()

    def handle_task(self, task_id):
        try:
            task = self.task_service.get_task(task_id)
            self.task_view.show_task(task)
        except Exception as e:
            print(f"An error occurred: {e}")

    def submit_answer(self, task_id, user_answer):
        try:
            self.task_service.submit_answer(task_id, user_answer)
            self.task_view.submit_answer(task_id, user_answer)
        except Exception as e:
            print(f"An error occurred: {e}")

class AuthController:
    def __init__(self):
        self.auth_service = AuthService(UserRepository())
        self.auth_view = AuthView()

    def handle_auth(self):
        try:
            username, password = self.auth_view.register_user()
            self.auth_service.register_user(username, password)
        except Exception as e:
            print(f"An error occurred: {e}")

    def handle_login(self):
        try:
            username, password = self.auth_view.login_user()
            self.auth_service.login_user(username, password)
        except Exception as e:
            print(f"An error occurred: {e}")

class MaterialController:
    def __init__(self):
        self.material_service = MaterialService(MaterialRepository())
        self.material_view = MaterialView()

    def handle_material(self, material_id):
        try:
            material = self.material_service.get_material(material_id)
            self.material_view.show_material(material)
        except Exception as e:
            print(f"An error occurred: {e}")

    def search_materials(self, tag):
        try:
            self.material_service.search_materials(tag)
            self.material_view.search_materials(tag)
        except Exception as e:
            print(f"An error occurred: {e}")

class ProgressController:
    def __init__(self):
        self.progress_service = ProgressService(ProgressRepository())
        self.progress_view = ProgressView()

    def handle_progress(self, user_id):
        try:
            progress = self.progress_service.get_progress(user_id)
            self.progress_view.show_progress(progress)
        except Exception as e:
            print(f"An error occurred: {e}")

    def save_progress(self, user_id, task_id, score, rating):
        try:
            self.progress_service.save_progress(user_id, task_id, score, rating)
        except Exception as e:
            print(f"An error occurred: {e}")

class FeedbackController:
    def __init__(self, progress_controller):
        self.feedback_service = FeedbackService(FeedbackRepository())
        self.feedback_view = FeedbackView()
        self.progress_controller = progress_controller

    def handle_feedback(self, user_id):
        try:
            comment, rating = self.feedback_view.submit_feedback()
            task_id = input("Введите ID задания для рейтинга: ")
            self.feedback_service.submit_feedback(user_id, comment, rating)
            self.progress_controller.save_progress(user_id, task_id, score=None, rating=rating)
        except Exception as e:
            print(f"An error occurred: {e}")

    def show_feedback(self, user_id):
        try:
            feedback = self.feedback_service.get_feedback(user_id)
            self.feedback_view.show_feedback(feedback)
        except Exception as e:
            print(f"An error occurred: {e}")

# Основной контроллер приложения
class Application:
    def __init__(self):
        self.task_controller = TaskController()
        self.auth_controller = AuthController()
        self.material_controller = MaterialController()
        self.progress_controller = ProgressController()
        self.feedback_controller = FeedbackController(self.progress_controller)

    def run(self):
        while True:
            print("Главное меню:")
            print("1. Регистрация")
            print("2. Вход")
            print("3. Задания")
            print("4. Материалы")
            print("5. Прогресс")
            print("6. Обратная связь")
            print("7. Выход")
            choice = input("Выберите действие: ")

            if choice == '1':
                self.auth_controller.handle_auth()
            elif choice == '2':
                self.auth_controller.handle_login()
            elif choice == '3':
                task_id = input("Введите ID задания: ")
                self.task_controller.handle_task(task_id)
            elif choice == '4':
                material_id = input("Введите ID материала: ")
                self.material_controller.handle_material(material_id)
            elif choice == '5':
                user_id = input("Введите ID пользователя: ")
                self.progress_controller.handle_progress(user_id)
            elif choice == '6':
                user_id = input("Введите ID пользователя: ")
                self.feedback_controller.handle_feedback(user_id)
            elif choice == '7':
                break
            else:
                print("Неверный выбор")

if __name__ == '__main__':
    app = Application()
    app.run()
