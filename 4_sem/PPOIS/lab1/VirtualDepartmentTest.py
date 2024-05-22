import unittest

from VirtualDepartment import (VirtualDepartment, Student, Teacher, LearningMaterial, Assignment, Test)

class TestVirtualDepartment(unittest.TestCase):

    def setUp(self):
        self.department = VirtualDepartment("ИИТ")
        self.teacher = Teacher(1, "Садовский")
        self.student = Student(1, "Телица", self.department)
        self.learning_material = LearningMaterial("Основы Python", "Статья о Python.")
        self.assignment = Assignment("Лабораторная 1", "Написать код.")
        self.test = Test("Тест 1", ["Вопрос 1", "Вопрос 2"])

    def test_add_student(self):
        self.department.add_student(self.student)
        self.assertIn(self.student.id, self.department.students)
        self.assertEqual(self.department.students[self.student.id], self.student)

    def test_remove_student(self):
        self.department.add_student(self.student)
        self.department.remove_student(self.student.id)
        self.assertNotIn(self.student.id, self.department.students)

    def test_add_teacher(self):
        self.department.add_teacher(self.teacher)
        self.assertIn(self.teacher.id, self.department.teachers)
        self.assertEqual(self.department.teachers[self.teacher.id], self.teacher)

    def test_remove_teacher(self):
        self.department.add_teacher(self.teacher)
        self.department.remove_teacher(self.teacher.id)
        self.assertNotIn(self.teacher.id, self.department.teachers)

    def test_add_learning_material(self):
        self.department.add_learning_material(self.learning_material)
        self.assertIn(self.learning_material, self.department.learning_materials)

    def test_remove_learning_material(self):
        self.department.add_learning_material(self.learning_material)
        self.department.remove_learning_material(self.learning_material.title)
        self.assertNotIn(self.learning_material, self.department.learning_materials)

    def test_add_assignment(self):
        self.department.add_assignment(self.assignment)
        self.assertIn(self.assignment, self.department.assignments)

    def test_remove_assignment(self):
        self.department.add_assignment(self.assignment)
        self.department.remove_assignment(self.assignment.title)
        self.assertNotIn(self.assignment, self.department.assignments)

    def test_add_test(self):
        self.department.add_test(self.test)
        self.assertIn(self.test, self.department.tests)

    def test_remove_test(self):
        self.department.add_test(self.test)
        self.department.remove_test(self.test.title)
        self.assertNotIn(self.test, self.department.tests)

    def test_conduct_online_lecture(self):
        lecture = self.teacher.conduct_online_lecture("Лекция по Python", [self.student])
        self.department.conduct_online_lecture(lecture)
        self.assertIn(lecture, self.department.online_lectures)

    def test_view_completed_lectures(self):
        lecture = self.teacher.conduct_online_lecture("Лекция по Python", [self.student])
        self.department.conduct_online_lecture(lecture)
        lectures_info = self.department.view_completed_lectures()
        self.assertEqual(len(lectures_info), 1)
        self.assertEqual(lectures_info[0], (self.teacher.full_name, lecture.topic, [self.student.full_name]))

    def test_view_available_tests(self):
        self.department.add_test(self.test)
        available_tests = self.department.view_available_tests()
        self.assertIn(self.test.title, available_tests)

    def test_view_available_assignments(self):
        self.department.add_assignment(self.assignment)
        available_assignments = self.department.view_available_assignments()
        self.assertIn(self.assignment.title, available_assignments)

    def test_view_learning_materials(self):
        self.department.add_learning_material(self.learning_material)
        learning_materials = self.department.view_learning_materials()
        self.assertIn(self.learning_material.title, learning_materials)

    def test_student_complete_assignment(self):
        self.department.add_assignment(self.assignment)
        self.student.complete_assignment(self.assignment.title, "Моя работа")
        self.assertIn(self.assignment.title, self.student.view_completed_assignments())

    def test_student_complete_test(self):
        self.department.add_test(self.test)
        self.student.complete_test(self.test.title, ["Ответ 1", "Ответ 2"])
        self.assertIn(self.test.title, self.student.view_completed_tests())

    def test_forum_create_thread(self):
        self.department.forum.create_thread(self.student, "Тема 1", "Описание темы 1")
        threads = self.department.forum.view_all_threads()
        self.assertEqual(len(threads), 1)
        self.assertEqual(threads[0], ("Тема 1", self.student.full_name))

    def test_forum_add_post(self):
        self.department.forum.create_thread(self.student, "Тема 1", "Описание темы 1")
        self.department.forum.add_post("Тема 1", self.teacher, "Ответ на тему 1")
        posts = self.department.forum.view_thread_posts("Тема 1")
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0], (self.teacher.full_name, "Ответ на тему 1"))

if __name__ == "__main__":
    unittest.main()
