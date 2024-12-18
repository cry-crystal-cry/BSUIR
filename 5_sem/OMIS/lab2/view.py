class TaskView:
    def show_task(self, task):
        print(f"Задание: {task['description']}")

    def submit_answer(self, task_id, user_answer):
        print(f"Ответ на задание {task_id}: {user_answer}")

class AuthView:
    def register_user(self):
        username = input("Введите имя пользователя: ")
        password = input("Введите пароль: ")
        return username, password

    def login_user(self):
        username = input("Введите имя пользователя: ")
        password = input("Введите пароль: ")
        return username, password

class MaterialView:
    def show_material(self, material):
        print(f"Материал: {material['description']}")

    def search_materials(self, tag):
        print(f"Поиск материалов по тегу: {tag}")

class ProgressView:
    def show_progress(self, progress):
        if not progress:
            print("Прогресс отсутствует.")
            return
        print("Прогресс:")
        print("ID | User ID | Task ID | Score | Rating")
        print("----------------------------------------")
        for item in progress:
            print(f"{item[0]} | {item[1]} | {item[2]} | {item[3]} | {item[4]}")

class FeedbackView:
    def submit_feedback(self):
        comment = input("Введите комментарий: ")
        rating = input("Введите рейтинг: ")
        return comment, rating

    def show_feedback(self, feedback):
        if not feedback:
            print("Обратная связь отсутствует.")
            return
        print("Обратная связь:")
        print("ID | User ID | Comment | Rating")
        print("---------------------------------")
        for item in feedback:
            print(f"{item[0]} | {item[1]} | {item[2]} | {item[3]}")
