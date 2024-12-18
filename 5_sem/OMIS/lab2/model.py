import sqlite3

# Репозитории
class TaskRepository:
    def __init__(self):
        self.conn = sqlite3.connect('learning_system.db')
        self.cursor = self.conn.cursor()

    def get_task(self, task_id):
        self.cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        task = self.cursor.fetchone()
        return {"id": task[0], "description": task[1]} if task else None

class UserRepository:
    def __init__(self):
        self.conn = sqlite3.connect('learning_system.db')
        self.cursor = self.conn.cursor()

    def get_user(self, user_id):
        self.cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = self.cursor.fetchone()
        return {"id": user[0], "username": user[1], "password": user[2]} if user else None

    def create_user(self, username, password):
        self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        self.conn.commit()

class MaterialRepository:
    def __init__(self):
        self.conn = sqlite3.connect('learning_system.db')
        self.cursor = self.conn.cursor()

    def get_material(self, material_id):
        self.cursor.execute("SELECT * FROM materials WHERE id = ?", (material_id,))
        material = self.cursor.fetchone()
        return {"id": material[0], "description": material[1]} if material else None

class ProgressRepository:
    def __init__(self):
        self.conn = sqlite3.connect('learning_system.db')
        self.cursor = self.conn.cursor()

    def save_progress(self, user_id, task_id, score, rating):
        self.cursor.execute("INSERT INTO progress (user_id, task_id, score, rating) VALUES (?, ?, ?, ?)", (user_id, task_id, score, rating))
        self.conn.commit()

    def get_progress(self, user_id):
        self.cursor.execute("SELECT * FROM progress WHERE user_id = ?", (user_id,))
        progress = self.cursor.fetchall()
        return progress

class FeedbackRepository:
    def __init__(self):
        self.conn = sqlite3.connect('learning_system.db')
        self.cursor = self.conn.cursor()

    def submit_feedback(self, user_id, comment, rating):
        self.cursor.execute("INSERT INTO feedback (user_id, comment, rating) VALUES (?, ?, ?)", (user_id, comment, rating))
        self.conn.commit()

    def get_feedback(self, user_id):
        self.cursor.execute("SELECT * FROM feedback WHERE user_id = ?", (user_id,))
        feedback = self.cursor.fetchall()
        return feedback

# Сервисы
class TaskService:
    def __init__(self, task_repository):
        self.task_repository = task_repository

    def get_task(self, task_id):
        return self.task_repository.get_task(task_id)

    def submit_answer(self, task_id, user_answer):
        pass

class AuthService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def register_user(self, username, password):
        self.user_repository.create_user(username, password)

    def login_user(self, username, password):
        pass

class MaterialService:
    def __init__(self, material_repository):
        self.material_repository = material_repository

    def get_material(self, material_id):
        return self.material_repository.get_material(material_id)

    def search_materials(self, tag):
        pass

class ProgressService:
    def __init__(self, progress_repository):
        self.progress_repository = progress_repository

    def save_progress(self, user_id, task_id, score, rating):
        self.progress_repository.save_progress(user_id, task_id, score, rating)

    def get_progress(self, user_id):
        return self.progress_repository.get_progress(user_id)

class FeedbackService:
    def __init__(self, feedback_repository):
        self.feedback_repository = feedback_repository

    def submit_feedback(self, user_id, comment, rating):
        self.feedback_repository.submit_feedback(user_id, comment, rating)

    def get_feedback(self, user_id):
        return self.feedback_repository.get_feedback(user_id)
