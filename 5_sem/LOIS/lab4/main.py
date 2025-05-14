# Лабораторная работа №2 по дисциплине Логические основы интеллектуальных систем
# Вариант 3: Запрограммировать обратный нечеткий логический вывод на основе операции нечеткой композиции (max({max({0}U{xi+yi-1})|i})).
# Выполнили студенты группы 221701: Телица И.Д., Карпук М.В.
# Программа выполняет обратный нечёткий логический вывод, содержит функцию запуска программы.
# Дата выполнения: 09.12.2024
# Источник: Блюмин С.Л., Шуйкова И.А., Сараев П.В. Нечеткая логика: алгебраические основы и приложения. — М.: Издательство, 2021. — 250 с.
# Источник: https://sanse.ru/index.php/sanse/article/download/331/290/579
import itertools
import numpy as np
from parser_data import parse_data


def print_reg(regions_):
    if not regions_:
        print("\nНет решений.")
    else:
        print("\nВыходные данные программы:")
        ranges = []
        for lb, ub in regions_:
            range_expr = " * ".join(
                [f"[{lb[j]:.1f}, {ub[j]:.1f}]" for j in range(len(lb))]
            )
            ranges.append(f"({range_expr})")

        union_ranges = " ∪ \n ∪ ".join(ranges)

        variables = ", ".join([f"B(x_{j + 1})" for j in range(len(lb))])

        print(f"<{variables}> ∈ {union_ranges}")


def generate_combinations(N, K):
    n, m = N.shape
    pattern_choices = []
    for i in range(n):
        if K[i] == 0:
            pattern_choices.append([None])
        else:
            pattern_choices.append(list(range(m)))
    return itertools.product(*pattern_choices), m


def initialize_bounds(m):
    return np.zeros(m), np.ones(m)


def update_bounds_for_k0(N, i, lower_bounds, upper_bounds):
    for j in range(len(lower_bounds)):
        ub_new = 1 - N[i, j]
        if ub_new < upper_bounds[j]:
            upper_bounds[j] = ub_new
        if lower_bounds[j] > upper_bounds[j]:
            return False
    return True


def update_bounds_for_ki(N, i, chosen_j, K, lower_bounds, upper_bounds):
    x_val = 1 - N[i, chosen_j] + K[i]
    if x_val < lower_bounds[chosen_j] or x_val > upper_bounds[chosen_j]:
        return False

    lower_bounds[chosen_j] = max(lower_bounds[chosen_j], x_val)
    upper_bounds[chosen_j] = min(upper_bounds[chosen_j], x_val)

    if lower_bounds[chosen_j] > upper_bounds[chosen_j]:
        return False

    for j in range(len(lower_bounds)):
        if j == chosen_j:
            continue
        potential_ub = 1 - N[i, j] + K[i]
        if potential_ub < upper_bounds[j]:
            upper_bounds[j] = potential_ub
        if lower_bounds[j] > upper_bounds[j]:
            return False
    return True


def validate_bounds(lower_bounds, upper_bounds):
    for j in range(len(lower_bounds)):
        if upper_bounds[j] < 0 or lower_bounds[j] > 1:
            return False
        lower_bounds[j] = max(lower_bounds[j], 0)
        upper_bounds[j] = min(upper_bounds[j], 1)
        if lower_bounds[j] > upper_bounds[j]:
            return False
    return True


def filter_unique_regions(solution_regions):
    unique_solutions = set()
    filtered_regions = []
    for lb, ub in solution_regions:
        key = (tuple(np.round(lb, decimals=10)), tuple(np.round(ub, decimals=10)))
        if key not in unique_solutions:
            unique_solutions.add(key)
            filtered_regions.append((lb, ub))
    return filtered_regions


def remove_contained_regions(filtered_regions):
    def is_contained(inner_lb, inner_ub, outer_lb, outer_ub):
        return np.all(outer_lb <= inner_lb) and np.all(inner_ub <= outer_ub)

    final_solutions = []
    for i, (lb_i, ub_i) in enumerate(filtered_regions):
        contained = False
        for j, (lb_j, ub_j) in enumerate(filtered_regions):
            if i != j and is_contained(lb_i, ub_i, lb_j, ub_j):
                contained = True
                break
        if not contained:
            final_solutions.append((lb_i, ub_i))
    return final_solutions


def solve_intervals(N, K):
    all_combinations, m = generate_combinations(N, K)
    solution_regions = []

    for combo in all_combinations:
        lower_bounds, upper_bounds = initialize_bounds(m)
        feasible = True

        for i, chosen_j in enumerate(combo):
            if K[i] == 0:
                if not update_bounds_for_k0(N, i, lower_bounds, upper_bounds):
                    feasible = False
                    break
            else:
                if not update_bounds_for_ki(N, i, chosen_j, K, lower_bounds, upper_bounds):
                    feasible = False
                    break

        if feasible and validate_bounds(lower_bounds, upper_bounds):
            solution_regions.append((lower_bounds.copy(), upper_bounds.copy()))

    filtered_regions = filter_unique_regions(solution_regions)
    final_solutions = remove_contained_regions(filtered_regions)

    return final_solutions



def main():
    files = ["test1.txt", "test2.txt", "test3.txt"]
    for file_name in files:
        print(f"file: {file_name}\n")

        array, matrix = parse_data(file_name)

        A = np.array(matrix)
        A = np.transpose(A)

        c = list(array.values())
        c = np.array(c)

        regions = solve_intervals(A, c)
        print_reg(regions)
        print("\n-------------------------\n")



if __name__ == "__main__":
    main()
