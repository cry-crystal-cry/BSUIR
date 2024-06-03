import xml.sax
import xml.dom.minidom
from typing import List, Optional


class Student:
    def __init__(self, fio, group, social_work):
        self.fio = fio
        self.group = group
        self.social_work = social_work


class StudentsSAXHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.students = []
        self.current_data = ""
        self.current_student = None
        self.social_work = []

    def startElement(self, tag, attributes):
        self.current_data = tag
        if tag == "student":
            self.current_student = Student("", "", [])

    def endElement(self, tag):
        if self.current_data == "fio":
            self.current_student.fio = self.content
        elif self.current_data == "group":
            self.current_student.group = self.content
        elif self.current_data == "semester":
            self.social_work.append(int(self.content))
        if tag == "social_work":
            self.current_student.social_work = self.social_work
            self.social_work = []
        elif tag == "student":
            self.students.append(self.current_student)
        self.current_data = ""

    def characters(self, content):
        self.content = content.strip()


class StudentsModel:
    def __init__(self):
        self.students = []

    def load_students(self, file_path):
        handler = StudentsSAXHandler()
        parser = xml.sax.make_parser()
        parser.setContentHandler(handler)
        parser.parse(file_path)
        self.students = handler.students

    def save_students(self, file_path):
        impl = xml.dom.minidom.getDOMImplementation()
        doc = impl.createDocument(None, "students", None)
        root = doc.documentElement

        for student in self.students:
            student_element = doc.createElement("student")

            fio_element = doc.createElement("fio")
            fio_text = doc.createTextNode(student.fio)
            fio_element.appendChild(fio_text)
            student_element.appendChild(fio_element)

            group_element = doc.createElement("group")
            group_text = doc.createTextNode(student.group)
            group_element.appendChild(group_text)
            student_element.appendChild(group_element)

            social_work_element = doc.createElement("social_work")
            for semester in student.social_work:
                semester_element = doc.createElement("semester")
                semester_text = doc.createTextNode(str(semester))
                semester_element.appendChild(semester_text)
                social_work_element.appendChild(semester_element)
            student_element.appendChild(social_work_element)

            root.appendChild(student_element)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(doc.toprettyxml(indent="  "))

    def add_student(self, student):
        self.students.append(student)

    def delete_students(self, fio: Optional[str] = None, group: Optional[str] = None, work_min: Optional[int] = None,
                        work_max: Optional[int] = None):
        def student_matches(student: Student) -> bool:
            if fio and fio not in student.fio:
                return False
            if group and group != student.group:
                return False
            if work_min is not None and work_max is not None and not (work_min <= max(student.social_work) <= work_max):
                return False
            return True

        deleted_count = 0
        for student in self.students:
            if student_matches(student):
                deleted_count += 1
        self.students = [student for student in self.students if not student_matches(student)]
        return deleted_count

    def search_students(self, fio: Optional[str] = None, group: Optional[str] = None, work_min: Optional[int] = None,
                        work_max: Optional[int] = None) -> List[Student]:
        def student_matches(student: Student) -> bool:
            if fio and fio not in student.fio:
                return False
            if group and group != student.group:
                return False
            if work_min is not None and work_max is not None and not (work_min <= max(student.social_work) <= work_max):
                return False
            return True

        return [student for student in self.students if student_matches(student)]

    def get_groups(self) -> List[str]:
        return list(set(student.group for student in self.students))
