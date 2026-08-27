# Индивидуальная лабораторная работа 2 по дисциплине МРЗвИС вариант 5
# Выполнена студентом группы 221701 БГУИР Телицей Ильей Денисовичем
# Файл создающий графики зависимостей параметров реализованной сети

# Использованные источники:
# Формальные модели обработки информации и параллельные модели решения задач. Практикум: учебно-методическое пособие / В.П.Ивашенко. – Минск: БГУИР, 2020.

import numpy as np
import matplotlib.pyplot as plt
from model import HopfieldNetwork
from utils import add_noise


def get_random_patterns(n_patterns, size):
    """Генерирует случайные образы {-1, 1}"""
    return np.random.choice([-1, 1], size=(n_patterns, size * size))


def run_test(n_patterns, img_side, noise_level, max_epochs=50):
    """Запускает один цикл: обучение -> зашумление -> восстановление"""
    patterns = get_random_patterns(n_patterns, img_side)
    net = HopfieldNetwork()
    net.train(patterns)

    # Берем первый образ для теста
    original = patterns[0]
    corrupted = add_noise(original, noise_level)

    # Получаем итерации
    _, iters = net.predict(corrupted, max_epochs)
    return iters

def plot_iters_vs_size():
    print("Запуск: Итерации vs Размер изображения")
    sizes = range(10, 61, 10)
    results = []

    for s in sizes:
        batch_iters = [run_test(n_patterns=10, img_side=s, noise_level=0.35) for _ in range(5)]
        results.append(np.mean(batch_iters))
        print(f"  Размер {s}x{s} готов")

    plt.figure(figsize=(8, 5))
    plt.plot([s * s for s in sizes], results, marker='s', color='blue')
    plt.xlabel("Размер изображения (в пикселях)")
    plt.ylabel("Среднее число итераций")
    plt.title("Зависимость итераций от размера изображения")
    plt.grid(True)
    plt.show()


def plot_iters_vs_noise():
    print("Запуск: Итерации vs Шум")
    noise_levels = np.linspace(0.1, 0.6, 6)
    results = []

    for nl in noise_levels:
        batch_iters = [run_test(n_patterns=10, img_side=28, noise_level=nl) for _ in range(5)]
        results.append(np.mean(batch_iters))
        print(f"  Шум {nl:.2f} готов")

    plt.figure(figsize=(8, 5))
    plt.plot(noise_levels, results, marker='o', color='red')
    plt.xlabel("Уровень шума")
    plt.ylabel("Среднее число итераций")
    plt.title("Зависимость количества итераций от уровня шума")
    plt.grid(True)
    plt.show()


def plot_iters_vs_capacity():
    print("Запуск: Итерации vs Кол-во образов")
    counts = [1, 10, 20, 35, 50, 100, 150, 200, 250]
    results = []

    for c in counts:
        batch_iters = [run_test(n_patterns=c, img_side=28, noise_level=0.35) for _ in range(5)]
        results.append(np.mean(batch_iters))
        print(f"  Образов: {c} готово")

    plt.figure(figsize=(8, 5))
    plt.plot(counts, results, marker='^', color='green')
    plt.xlabel("Количество запомненных образов")
    plt.ylabel("Среднее число итераций")
    plt.title("Зависимость итераций от количества образов")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":

    plot_iters_vs_size()
    plot_iters_vs_noise()
    plot_iters_vs_capacity()