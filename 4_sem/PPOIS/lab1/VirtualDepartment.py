from typing import List, Dict, Tuple, Any


class VirtualDepartment:
    def __init__(self, name: str):
        self.name: str = name
        self.students: Dict[int, Student] = {}
        self.teachers: Dict[int, Teacher] = {}
        self.learning_materials: List[LearningMaterial] = []
        self.assignments: List[Assignment] = []
        self.tests: List[Test] = []
        self.forum: Forum = Forum()
        self.online_lectures: List[OnlineLecture] = []

    def add_student(self, student: 'Student') -> None:
        if student.id in self.students:
            raise ValueError(f"Студент с id {student.id} уже существует.")
        self.students[student.id] = student

    def remove_student(self, student_id: int) -> None:
        if student_id not in self.students:
            raise ValueError(f"Студент с id {student_id} не найден.")
        del self.students[student_id]

    def add_teacher(self, teacher: 'Teacher') -> None:
        if teacher.id in self.teachers:
            raise ValueError(f"Преподаватель с id {teacher.id} уже существует.")
        self.teachers[teacher.id] = teacher

    def remove_teacher(self, teacher_id: int) -> None:
        if teacher_id not in self.teachers:
            raise ValueError(f"Преподаватель с id {teacher_id} не найден.")
        del self.teachers[teacher_id]

    def add_learning_material(self, material: 'LearningMaterial') -> None:
        self.learning_materials.append(material)

    def remove_learning_material(self, title: str) -> None:
        for material in self.learning_materials:
            if material.title == title:
                self.learning_materials.remove(material)
                return
        raise ValueError(f"Учебный материал с заголовком {title} не найден.")

    def add_assignment(self, assignment: 'Assignment') -> None:
        self.assignments.append(assignment)

    def remove_assignment(self, title: str) -> None:
        for assignment in self.assignments:
            if assignment.title == title:
                self.assignments.remove(assignment)
                return
        raise ValueError(f"Задание с заголовком {title} не найдено.")

    def add_test(self, test: 'Test') -> None:
        self.tests.append(test)

    def remove_test(self, title: str) -> None:
        for test in self.tests:
            if test.title == title:
                self.tests.remove(test)
                return
        raise ValueError(f"Тест с заголовком {title} не найден.")

    def conduct_online_lecture(self, lecture: 'OnlineLecture') -> None:
        self.online_lectures.append(lecture)

    def view_completed_lectures(self) -> List[Tuple[str, str, List[str]]]:
        lectures_info: List[Tuple[str, str, List[str]]] = []
        for lecture in self.online_lectures:
            participants = [student.full_name for student in lecture.students_present]
            lectures_info.append((lecture.teacher.full_name, lecture.topic, participants))
        return lectures_info

    def view_available_tests(self) -> List[str]:
        return [test.title for test in self.tests]

    def view_available_assignments(self) -> List[str]:
        return [assignment.title for assignment in self.assignments]

    def view_learning_materials(self) -> List[str]:
        return [material.title for material in self.learning_materials]


class User:
    def __init__(self, id: int, full_name: str):
        self.id: int = User.check_id(id)
        self.full_name: str = full_name

    @staticmethod
    def check_id(id: int) -> int:
        try:
            id = int(id)
        except Exception:
            raise ValueError("ID должно быть целым положительным числом.")
        if id <= 0:
            raise ValueError("ID должно быть целым положительным числом.")
        return id


class Student(User):
    def __init__(self, id: int, full_name: str, department: VirtualDepartment):
        super().__init__(id, full_name)
        self.department: VirtualDepartment = department
        self.completed_assignments: List[str] = []
        self.completed_tests: Dict[str, Any] = {}

    def complete_assignment(self, assignment_title: str, submission: Any) -> None:
        for assignment in self.department.assignments:
            if assignment.title == assignment_title:
                assignment.submit(self, submission)
                self.completed_assignments.append(assignment_title)
                return
        raise ValueError(f"Задание '{assignment_title}' не найдено.")

    def complete_test(self, test_title: str, answers: Any) -> None:
        for test in self.department.tests:
            if test.title == test_title:
                test.submit(self, answers)
                self.completed_tests[test_title] = answers
                return
        raise ValueError(f"Тест '{test_title}' не найден.")

    def view_completed_assignments(self) -> List[str]:
        return self.completed_assignments

    def view_completed_tests(self) -> List[str]:
        return list(self.completed_tests.keys())


class Teacher(User):
    def __init__(self, id: int, full_name: str):
        super().__init__(id, full_name)

    def create_assignment(self, title: str, description: str) -> 'Assignment':
        return Assignment(title, description)

    def create_test(self, title: str, questions: List[str]) -> 'Test':
        return Test(title, questions)

    def conduct_online_lecture(self, topic: str, students_present: List[Student]) -> 'OnlineLecture':
        return OnlineLecture(self, topic, students_present)


class LearningMaterial:
    def __init__(self, title: str, content: str):
        self.title: str = title
        self.content: str = content


class Assignment:
    def __init__(self, title: str, description: str):
        self.title: str = title
        self.description: str = description
        self.submissions: Dict[int, Any] = {}

    def submit(self, student: Student, submission: Any) -> None:
        self.submissions[student.id] = submission


class Test:
    def __init__(self, title: str, questions: List[str]):
        self.title: str = title
        self.questions: List[str] = questions
        self.submissions: Dict[int, Any] = {}

    def submit(self, student: Student, answers: Any) -> None:
        self.submissions[student.id] = answers


class Forum:
    def __init__(self):
        self.threads: List[ForumThread] = []

    def create_thread(self, author: User, title: str, content: str) -> None:
        thread = ForumThread(author, title, content)
        self.threads.append(thread)

    def add_post(self, thread_title: str, author: User, content: str) -> None:
        for thread in self.threads:
            if thread.title == thread_title:
                thread.add_post(author, content)
                return
        raise ValueError(f'Тема {thread_title} не найдена.')

    def view_all_threads(self) -> List[Tuple[str, str]]:
        return [(thread.title, thread.author.full_name) for thread in self.threads]

    def view_thread_posts(self, thread_title: str) -> List[Tuple[str, str]]:
        for thread in self.threads:
            if thread.title == thread_title:
                return [(post.author.full_name, post.content) for post in thread.posts]
        raise ValueError(f"Тема с заголовком '{thread_title}' не найдена.")


class ForumThread:
    def __init__(self, author: User, title: str, content: str):
        self.author: User = author
        self.title: str = title
        self.content: str = content
        self.posts: List[ForumPost] = []

    def add_post(self, author: User, content: str) -> None:
        self.posts.append(ForumPost(author, content))


class ForumPost:
    def __init__(self, author: User, content: str):
        self.author: User = author
        self.content: str = content


class OnlineLecture:
    def __init__(self, teacher: Teacher, topic: str, students_present: List[Student]):
        self.teacher: Teacher = teacher
        self.topic: str = topic
        self.students_present: List[Student] = students_present


def main():
    department_name = input("Введите название кафедры: ")
    department = VirtualDepartment(department_name)
    print(f'Виртуальная кафедра {department_name} создана')

    while True:
        print("\nМеню:")
        print("1. Добавить студента")
        print("2. Добавить преподавателя")
        print("3. Создать задание")
        print("4. Создать тест")
        print("5. Провести онлайн лекцию")
        print("6. Удалить студента")
        print("7. Удалить преподавателя")
        print("8. Удалить задание")
        print("9. Удалить тест")
        print("10. Добавить учебный материал")
        print("11. Удалить учебный материал")
        print("12. Пройти тест")
        print("13. Выполнить задание")
        print("14. Просмотреть доступные тесты")
        print("15. Просмотреть доступные задания")
        print("16. Просмотреть доступные учебные материалы")
        print("17. Просмотреть выполненные задания студента")
        print("18. Просмотреть пройденные тесты студента")
        print("19. Создать тему на форуме")
        print("20. Добавить пост в тему на форуме")
        print("21. Просмотреть пройденные лекции и их участников")
        print("22. Просмотреть все темы на форуме")
        print("23. Просмотреть все посты в теме на форуме")
        print("24. Выйти")

        choice = input("Выберите действие: ")

        if choice == "1":
            try:
                id = User.check_id(input("Введите id студента: "))
                full_name = input("Введите ФИО студента: ")
                student = Student(id, full_name, department)
                department.add_student(student)
                print(f"Студент {full_name} добавлен.")
            except ValueError as e:
                print(e)

        elif choice == "2":
            try:
                id = User.check_id(input("Введите id преподавателя: "))
                full_name = input("Введите ФИО преподавателя: ")
                teacher = Teacher(id, full_name)
                department.add_teacher(teacher)
                print(f"Преподаватель {full_name} добавлен.")
            except ValueError as e:
                print(e)

        elif choice == "3":
            try:
                teacher_id = User.check_id(input("Введите id преподавателя, создающего задание: "))
                if teacher_id in department.teachers:
                    teacher = department.teachers[teacher_id]
                    title = input("Введите название задания: ")
                    description = input("Введите описание задания: ")
                    assignment = teacher.create_assignment(title, description)
                    department.add_assignment(assignment)
                    print(f"Задание {title} создано.")
                else:
                    raise ValueError("Преподаватель не найден.")
            except ValueError as e:
                print(e)

        elif choice == "4":
            try:
                teacher_id = User.check_id(input("Введите id преподавателя, создающего тест: "))
                if teacher_id in department.teachers:
                    teacher = department.teachers[teacher_id]
                    title = input("Введите название теста: ")
                    questions = {}
                    while True:
                        question = input("Введите вопрос (или 'стоп' для завершения): ")
                        if question.lower() == 'стоп':
                            break
                        answer = input("Введите ответ: ")
                        questions[question] = answer
                    test = teacher.create_test(title, questions)
                    department.add_test(test)
                    print(f"Тест {title} создан.")
                else:
                    raise ValueError("Преподаватель не найден.")
            except ValueError as e:
                print(e)

        elif choice == "5":
            try:
                teacher_id = User.check_id(input("Введите id преподавателя, проводящего лекцию: "))
                if teacher_id in department.teachers:
                    teacher = department.teachers[teacher_id]
                    topic = input("Введите тему лекции: ")
                    student_ids = input("Введите id студентов, присутствующих на лекции (через запятую): ").split(",")
                    students_present = []
                    for student_id in student_ids:
                        current_id = User.check_id(student_id)
                        if current_id in department.students:
                            students_present.append(department.students[current_id])
                    lecture = teacher.conduct_online_lecture(topic, students_present)
                    department.conduct_online_lecture(lecture)
                    print(f"Лекция на тему '{topic}' проведена.")
                else:
                    raise ValueError("Преподаватель не найден.")
            except ValueError as e:
                print(e)

        elif choice == "6":
            try:
                student_id = User.check_id(input("Введите id студента для удаления: "))
                department.remove_student(student_id)
                print(f"Студент с id {student_id} удален.")
            except ValueError as e:
                print(e)

        elif choice == "7":
            try:
                teacher_id = User.check_id(input("Введите id преподавателя для удаления: "))
                department.remove_teacher(teacher_id)
                print(f"Преподаватель с id {teacher_id} удален.")
            except ValueError as e:
                print(e)

        elif choice == "8":
            title = input("Введите название задания для удаления: ")
            try:
                department.remove_assignment(title)
                print(f"Задание '{title}' удалено.")
            except ValueError as e:
                print(e)

        elif choice == "9":
            title = input("Введите название теста для удаления: ")
            try:
                department.remove_test(title)
                print(f"Тест '{title}' удален.")
            except ValueError as e:
                print(e)

        elif choice == "10":
            title = input("Введите название учебного материала: ")
            content = input("Введите содержание учебного материала: ")
            material = LearningMaterial(title, content)
            department.add_learning_material(material)
            print(f"Учебный материал '{title}' добавлен.")

        elif choice == "11":
            title = input("Введите название учебного материала для удаления: ")
            try:
                department.remove_learning_material(title)
                print(f"Учебный материал '{title}' удален.")
            except ValueError as e:
                print(e)

        elif choice == "12":
            try:
                student_id = User.check_id(input("Введите id студента, проходящего тест: "))
                if student_id in department.students:
                    student = department.students[student_id]
                    test_title = input("Введите название теста: ")
                    answers = {}
                    for test in department.tests:
                        if test.title == test_title:
                            for question in test.questions:
                                answer = input(f"{question}: ")
                                answers[question] = answer
                            student.complete_test(test_title, answers)
                            print(f"Тест '{test_title}' пройден.")
                            break
                    else:
                        print("Тест не найден.")
                else:
                    print("Студент не найден.")
            except ValueError as e:
                print(e)

        elif choice == "13":
            try:
                student_id = User.check_id(input("Введите id студента, выполняющего задание: "))
                if student_id in department.students:
                    student = department.students[student_id]
                    assignment_title = input("Введите название задания: ")
                    submission = input("Введите выполнение задания: ")
                    student.complete_assignment(assignment_title, submission)
                    print(f"Задание '{assignment_title}' выполнено.")
                else:
                    print("Студент не найден.")
            except ValueError as e:
                print(e)

        elif choice == "14":
            print("Доступные тесты:")
            for test in department.view_available_tests():
                print(test)

        elif choice == "15":
            print("Доступные задания:")
            for assignment in department.view_available_assignments():
                print(assignment)

        elif choice == "16":
            print("Доступные учебные материалы:")
            for material in department.view_learning_materials():
                print(material)

        elif choice == "17":
            try:
                student_id = User.check_id(input("Введите id студента: "))
                if student_id in department.students:
                    student = department.students[student_id]
                    print("Выполненные задания:")
                    for assignment in student.view_completed_assignments():
                        print(assignment)
                else:
                    raise ValueError("Студент не найден.")
            except ValueError as e:
                print(e)

        elif choice == "18":
            try:
                student_id = User.check_id(input("Введите id студента: "))
                if student_id in department.students:
                    student = department.students[student_id]
                    print("Пройденные тесты:")
                    for test in student.view_completed_tests():
                        print(test)
                else:
                    raise ValueError("Студент не найден.")
            except ValueError as e:
                print(e)

        elif choice == "19":
            try:
                author_id = User.check_id(input("Введите id пользователя, создающего тему: "))
                user_type = input("Введите пользователя, создающего пост (студент\\преподаватель)")
                if user_type == "студент" and author_id in department.students:
                    author = department.students[author_id]
                elif user_type == "преподаватель" and author_id in department.teachers:
                    author = department.teachers[author_id]
                else:
                    raise ValueError("Пользователь не найден.")
                title = input("Введите название темы: ")
                content = input("Введите содержание темы: ")
                department.forum.create_thread(author, title, content)
                print(f"Тема '{title}' создана.")
            except ValueError as e:
                print(e)

        elif choice == "20":
            thread_title = input("Введите название темы для добавления поста: ")
            try:
                author_id = User.check_id(input("Введите id пользователя, добавляющего пост: "))
                user_type = input("Введите пользователя, создающего пост (студент\\преподаватель)")
                if user_type == "студент" and author_id in department.students:
                    author = department.students[author_id]
                elif user_type == "преподаватель" and author_id in department.teachers:
                    author = department.teachers[author_id]
                else:
                    raise ValueError("Пользователь не найден.")
                content = input("Введите содержание поста: ")
                department.forum.add_post(thread_title, author, content)
                print(f"Пост добавлен в тему '{thread_title}'.")
            except ValueError as e:
                print(e)

        if choice == "21":
            print("Пройденные лекции и их участники:")
            for lecture_info in department.view_completed_lectures():
                print(f"Преподаватель: {lecture_info[0]}")
                print(f"Тема лекции: {lecture_info[1]}")
                print("Участники:")
                for participant in lecture_info[2]:
                    print(f" - {participant}")

        elif choice == "22":
            print("Все темы на форуме:")
            for thread_title, author_name in department.forum.view_all_threads():
                print(f"Тема: {thread_title} (Автор: {author_name})")

        elif choice == "23":
            thread_title = input("Введите название темы: ")
            try:
                posts = department.forum.view_thread_posts(thread_title)
                print(f"Посты в теме '{thread_title}':")
                for author_name, content in posts:
                    print(f"{author_name}: {content}")
            except ValueError as e:
                print(e)

        elif choice == "24":
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
