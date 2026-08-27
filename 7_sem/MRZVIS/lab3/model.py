# Индивидуальная лабораторная работа 3 по дисциплине МРЗвИС вариант 5
# Выполнена студентом группы 221701 БГУИР Телицей Ильей Денисовичем
# Файл содержащий модель рекуррентной сети с цепью нейросетевых моделей долгой кратковременной памяти (LSTM) с функцией активации Leaky ReLU на скрытом слое
# Использованные источники:
# Формальные модели обработки информации и параллельные модели решения задач. Практикум: учебно-методическое пособие / В.П.Ивашенко. – Минск: БГУИР, 2020.


import numpy as np


class LSTMModel:
    def __init__(self, in_size, hidden_size, out_size, alpha=0.1):
        self.h_size = hidden_size
        self.alpha = alpha

        # На каждом шаге рекурсии подается 1 число
        input_dim = 1
        concat_size = input_dim + hidden_size

        # Инициализация весов gate-ов
        self.Wf = np.random.randn(hidden_size, concat_size) * np.sqrt(2 / concat_size) # инициализация Кайминга
        self.Wi = np.random.randn(hidden_size, concat_size) * np.sqrt(2 / concat_size)
        self.Wc = np.random.randn(hidden_size, concat_size) * np.sqrt(2 / concat_size)
        self.Wo = np.random.randn(hidden_size, concat_size) * np.sqrt(2 / concat_size)
        self.Wy = np.random.randn(out_size, hidden_size) * np.sqrt(2 / hidden_size)

        self.bf, self.bi = np.zeros((hidden_size, 1)), np.zeros((hidden_size, 1))
        self.bc, self.bo = np.zeros((hidden_size, 1)), np.zeros((hidden_size, 1))
        self.by = np.zeros((out_size, 1))

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))

    def leaky_relu(self, x):
        return np.where(x > 0, x, x * self.alpha)

    def d_leaky_relu(self, x):
        return np.where(x > 0, 1, self.alpha)

    def forward(self, x_seq):
        h, c, f, i, c_bar, o, x_concat = {}, {}, {}, {}, {}, {}, {}
        h[-1] = np.zeros((self.h_size, 1))
        c[-1] = np.zeros((self.h_size, 1))

        # Модель проходит через все элементы окна (их количество равно in_size)
        for t in range(len(x_seq)):
            xt = np.array([[x_seq[t]]])  # Текущее число из окна
            x_concat[t] = np.vstack((h[t - 1], xt))  # Склейка: (hidden + 1, 1)

            f[t] = self.sigmoid(np.dot(self.Wf, x_concat[t]) + self.bf)
            i[t] = self.sigmoid(np.dot(self.Wi, x_concat[t]) + self.bi)
            c_bar[t] = self.leaky_relu(np.dot(self.Wc, x_concat[t]) + self.bc)

            c[t] = f[t] * c[t - 1] + i[t] * c_bar[t]
            o[t] = self.sigmoid(np.dot(self.Wo, x_concat[t]) + self.bo)
            h[t] = o[t] * self.leaky_relu(c[t])

        # Финальный результат на основе последнего скрытого состояния
        y = np.dot(self.Wy, h[len(x_seq) - 1]) + self.by
        return y, (h, c, f, i, c_bar, o, x_concat)

    def train_step(self, x_seq, y_true, lr):
        y_pred, cache = self.forward(x_seq)
        h, c, f, i, c_bar, o, x_concat = cache
        T = len(x_seq)
        dy = y_pred - y_true.reshape(-1, 1)

        dWy = np.dot(dy, h[T - 1].T)
        dby = dy
        dh = np.dot(self.Wy.T, dy)
        dc = np.zeros_like(c[0])

        dWf, dWi, dWc, dWo = 0, 0, 0, 0
        dbf, dbi, dbc, dbo = 0, 0, 0, 0

        for t in reversed(range(T)):
            do = dh * self.leaky_relu(c[t])
            do_raw = do * o[t] * (1 - o[t])
            dc = dh * o[t] * self.d_leaky_relu(c[t]) + dc
            dc_bar = dc * i[t]
            dc_bar_raw = dc_bar * self.d_leaky_relu(np.dot(self.Wc, x_concat[t]) + self.bc)
            di = dc * c_bar[t]
            di_raw = di * i[t] * (1 - i[t])
            df = dc * c[t - 1]
            df_raw = df * f[t] * (1 - f[t])

            dWf += np.dot(df_raw, x_concat[t].T)
            dWi += np.dot(di_raw, x_concat[t].T)
            dWc += np.dot(dc_bar_raw, x_concat[t].T)
            dWo += np.dot(do_raw, x_concat[t].T)
            dbf += df_raw
            dbi += di_raw
            dbc += dc_bar_raw
            dbo += do_raw

            dc = f[t] * dc
            d_concat = (np.dot(self.Wf.T, df_raw) + np.dot(self.Wi.T, di_raw) +
                        np.dot(self.Wc.T, dc_bar_raw) + np.dot(self.Wo.T, do_raw))
            dh = d_concat[:self.h_size, :]

        for p, dp in zip([self.Wf, self.Wi, self.Wc, self.Wo, self.Wy, self.bf, self.bi, self.bc, self.bo, self.by],
                         [dWf, dWi, dWc, dWo, dWy, dbf, dbi, dbc, dbo, dby]):
            p -= lr * np.clip(dp, -1, 1)
        return np.mean(dy ** 2)
