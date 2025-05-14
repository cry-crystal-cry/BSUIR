# Лабораторная работа №2 по дисциплине Логические основы интеллектуальных систем
# Вариант 3: Запрограммировать обратный нечеткий логический вывод на основе операции нечеткой композиции (max({max({0}U{xi+yi-1})|i})).
# Выполнили студенты группы 221701: Телица И.Д., Карпук М.В.
# Файл, содержащий функции для чтения данных с тестовых файлов и преобразования в нужный формат
# Дата выполнения: 09.12.2024
# Источник: Блюмин С.Л., Шуйкова И.А., Сараев П.В. Нечеткая логика: алгебраические основы и приложения. — М.: Издательство, 2021. — 250 с.
# Источник: https://sanse.ru/index.php/sanse/article/download/331/290/579
import re


def check_range(value, name):
    if not (0.0 <= value <= 1.0):
        raise ValueError(f"Value {value} in {name} is out of range [0.0, 1.0]")


def parse_data(filename):
    with open(filename, 'r') as file:
        data = file.read()
    b_match = re.search(r"C=\{(.*?)\}", data, re.DOTALL)
    if b_match:
        b_content = b_match.group(1).strip()
        matches = re.findall(r"<(y\d+),\s*([\d.]+)>", b_content)
        C = {}
        for key, value in matches:
            value = float(value)
            check_range(value, f"C[{key}]")
            C[key] = value
    else:
        C = {}

    l_match = re.search(r"A=\(([\s\S]*?)\)", data)
    if l_match:
        l_rows = l_match.group(1).strip().split("\n")
        A = []
        for i, row in enumerate(l_rows):
            row_values = list(map(float, row.split()))
            for j, value in enumerate(row_values):
                check_range(value, f"A[{i}][{j}]")
            A.append(row_values)
    else:
        A = []

    if len(C) != len(A[0]):
        raise ValueError(f"len(C) != len(A)")

    print("Множество C:")
    print(C)
    print("\nМатрица A:")
    for row_ in A:
        print(row_)

    return C, A

