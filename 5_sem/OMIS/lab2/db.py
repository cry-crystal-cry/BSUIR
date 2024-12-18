import sqlite3

def init_db():
    try:
        conn = sqlite3.connect('learning_system.db')
        cursor = conn.cursor()

        # Создание таблиц
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS materials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                task_id INTEGER,
                score INTEGER,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (task_id) REFERENCES tasks (id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                comment TEXT,
                rating INTEGER,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

        # Добавление поля rating в таблицу progress, если оно еще не существует
        cursor.execute("PRAGMA table_info(progress)")
        columns = cursor.fetchall()
        column_names = [column[1] for column in columns]
        if 'rating' not in column_names:
            cursor.execute("ALTER TABLE progress ADD COLUMN rating INTEGER")

        # Наполнение таблиц начальными данными
        cursor.execute('''
            INSERT OR IGNORE INTO users (username, password) VALUES ('user1', 'password1')
        ''')

        cursor.execute('''
            INSERT OR IGNORE INTO tasks (description) VALUES ('Task 1 description')
        ''')

        cursor.execute('''
            INSERT OR IGNORE INTO tasks (description) VALUES ('Task 2 description')
        ''')

        cursor.execute('''
            INSERT OR IGNORE INTO materials (description) VALUES ('Material 1 description')
        ''')

        cursor.execute('''
            INSERT OR IGNORE INTO materials (description) VALUES ('Material 2 description')
        ''')

        conn.commit()
        print("Database initialized successfully.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

def print_db_info():
    try:
        conn = sqlite3.connect('learning_system.db')
        cursor = conn.cursor()

        # Получение информации о таблицах и полях
        tables = ['users', 'tasks', 'materials', 'progress', 'feedback']
        for table in tables:
            print(f"\nTable '{table}' info:")
            cursor.execute(f"PRAGMA table_info({table})")
            columns = cursor.fetchall()
            for column in columns:
                print(f"{column[1]} ({column[2]})")

        # Получение информации о пользователях
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        print("\nUsers in the database:")
        print("ID | Username | Password")
        print("------------------------")
        for user in users:
            print(f"{user[0]} | {user[1]} | {user[2]}")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    init_db()
    print_db_info()
