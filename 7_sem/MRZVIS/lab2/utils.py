# Индивидуальная лабораторная работа 2 по дисциплине МРЗвИС вариант 5
# Выполнена студентом группы 221701 БГУИР Телицей Ильей Денисовичем
# Файл, содержащий вспомогательные функции для работы с изображениями

# Использованные источники:
# Формальные модели обработки информации и параллельные модели решения задач. Практикум: учебно-методическое пособие / В.П.Ивашенко. – Минск: БГУИР, 2020.


import os

import numpy as np
import random
from PIL import Image
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")


def load_image(path, size=(28, 28)):
    """Загрузка изображения и перевод в {-1, 1}"""
    img = Image.open(path).convert('L').resize(size)
    arr = np.array(img)
    return np.where(arr > 127, 1, -1).flatten()


def add_noise(pattern, level=0.2):
    """Инвертирует случайные пиксели"""
    noisy = pattern.copy()
    n_changes = int(len(pattern) * level)
    indices = np.random.choice(len(pattern), n_changes, replace=False)
    for i in indices:
        # Для дискретного состояния {-1, 0, 1}
        choices = [-1, 0, 1]
        if noisy[i] in choices: choices.remove(noisy[i])
        noisy[i] = random.choice(choices)
    return noisy


def save_image(pattern, folder, filename, size=(28, 28)):
    """Преобразует вектор {-1, 1} в картинку и сохраняет"""
    os.makedirs(folder, exist_ok=True)
    img_arr = np.where(pattern.reshape(size) > 0, 255, 0).astype(np.uint8)
    img = Image.fromarray(img_arr)
    img.save(os.path.join(folder, filename))


def visualize_results(original, corrupted, restored, title="", shape=(28, 28)):
    fig, axes = plt.subplots(1, 3, figsize=(10, 3))
    fig.suptitle(title)
    imgs = [original, corrupted, restored]
    titles = ["Original", "Corrupted", "Restored"]
    for ax, img, t in zip(axes, imgs, titles):
        ax.imshow(img.reshape(shape), cmap='gray', vmin=-1, vmax=1)
        ax.set_title(t)
        ax.axis('off')
    plt.show()
