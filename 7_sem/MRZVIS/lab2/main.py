# Индивидуальная лабораторная работа 2 по дисциплине МРЗвИС вариант 5
# Выполнена студентом группы 221701 БГУИР Телицей Ильей Денисовичем
# Файл начала программы, реализующий процесс обработки входных данных

# Использованные источники:
# Формальные модели обработки информации и параллельные модели решения задач. Практикум: учебно-методическое пособие / В.П.Ивашенко. – Минск: БГУИР, 2020.

import os
import numpy as np
from model import HopfieldNetwork
from utils import load_image, save_image, add_noise, visualize_results

CONFIG = {
    "path_patterns": "patterns_digits",
    "path_corrupted": "corrupted",
    "path_restored": "restored",

    "img_size": (28, 28),

    "max_epochs": 20,
    "noise_level": 0.4,

    "show_plots": True,
}


def main():
    cfg = CONFIG

    if not os.path.exists(cfg["path_patterns"]):
        print(f"Ошибка: Папка {cfg['path_patterns']} не найдена.")
        return

    files = sorted([f for f in os.listdir(cfg["path_patterns"]) if f.endswith('.png')])
    if not files:
        print("Ошибка: В папке нет PNG файлов.")
        return

    print(f"--- Обучение на {len(files)} образах ---")
    patterns = np.array([load_image(os.path.join(cfg["path_patterns"], f), cfg["img_size"]) for f in files])

    net = HopfieldNetwork()
    net.train(patterns)

    total_pixels = cfg["img_size"][0] * cfg["img_size"][1]
    print(f"--- Начало восстановления (Шум: {cfg['noise_level'] * 100}%) ---")

    for i, filename in enumerate(files):
        original = patterns[i]

        corrupted = add_noise(original, cfg["noise_level"])

        restored, iters = net.predict(corrupted, cfg["max_epochs"])

        hamming_dist = np.count_nonzero(original != restored)
        similarity = (1 - hamming_dist / total_pixels) * 100

        save_image(corrupted, cfg["path_corrupted"], f"corr_{filename}", cfg["img_size"])
        save_image(restored, cfg["path_restored"], f"rest_{filename}", cfg["img_size"])

        print(f"Файл: {filename}")
        print(f"  > Итераций: {iters}")
        print(f"  > Расстояние Хэмминга: {hamming_dist} из {total_pixels} пикс.")
        print(f"  > Схожесть с оригиналом: {similarity:.2f}%")
        print("-" * 30)

        if cfg["show_plots"]:
            visualize_results(original, corrupted, restored)

    print(f"\nГотово! Результаты в папках '{cfg['path_corrupted']}' и '{cfg['path_restored']}'")


if __name__ == "__main__":
    main()