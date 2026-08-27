# Индивидуальная лабораторная работа 2 по дисциплине МРЗвИС вариант 5
# Выполнена студентом группы 221701 БГУИР Телицей Ильей Денисовичем
# Файл содержащий модель сети Хопфилда с дискретным состоянием и дискретным временем в асинхронном режиме

# Использованные источники:
# Формальные модели обработки информации и параллельные модели решения задач. Практикум: учебно-методическое пособие / В.П.Ивашенко. – Минск: БГУИР, 2020.


import numpy as np


class HopfieldNetwork:
    def __init__(self):
        self.weights = None
        self.n_neurons = None

    def train(self, patterns: np.ndarray):
        """
        Метод проекций: W = X * pinv(X)
        patterns: матрица (M, N), где M - кол-во образов, N - размерность
        """
        self.n_neurons = patterns.shape[1]
        X = patterns.T

        W = X @ np.linalg.pinv(X)

        # Обнуляем диагональ
        np.fill_diagonal(W, 0)
        self.weights = W

    def _activation(self, h, current_val):
        """Модифицированная функция знака"""
        if h > 0:
            return 1
        elif h < 0:
            return -1
        return current_val

    def predict(self, input_pattern: np.ndarray, max_epochs: int):
        state = input_pattern.copy().astype(float)
        iterations = 0
        for epoch in range(max_epochs):
            iterations += 1
            prev_state = state.copy()
            indices = np.random.permutation(self.n_neurons)
            for i in indices:
                h = np.dot(self.weights[i], state)
                state[i] = self._activation(h, state[i])

            if np.array_equal(state, prev_state):
                break
        return state, iterations
