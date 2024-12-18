import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


def my_fft(signal):
    x = signal
    N = len(x)
    if N <= 1:
        return x
    else:
        # Разделяем сигнал на четные и нечетные элементы
        even = my_fft(x[0::2])
        odd = my_fft(x[1::2])

        # Вычисляем коэффициенты Фурье
        kff = [np.exp(-2j * np.pi * k / N) * odd[k] for k in range(N // 2)]
        return ([even[k] + kff[k] for k in range(N // 2)]
                + [even[k] - kff[k] for k in range(N // 2)])


def generate_signal(function, frequency, length):
    t = np.linspace(0, 1, length, endpoint=False)
    if function == 'sin':
        signal = np.sin(2 * np.pi * frequency * t)
    elif function == 'cos':
        signal = np.cos(2 * np.pi * frequency * t)
    else:
        raise ValueError("Выберите либо 'sin', либо 'cos'")
    return signal


function = input("Введите функцию (sin или cos): ")
frequency = int(input("Введите частоту: "))
length = 235

signal = generate_signal(function, frequency, length)
next_pow_of_2 = 1 << (length - 1).bit_length()
signal = list(signal)
signal = signal + [0] * (next_pow_of_2 - length)
signal_after_my_fft = my_fft(signal)
signal_after_fft = np.fft.fft(signal)

# Построение графиков
plt.figure(figsize=(10, 9))

plt.subplot(3, 1, 1)
plt.plot(signal)
plt.title("Исходный сигнал")
plt.xlabel("Время")
plt.ylabel("Амплитуда")

plt.subplot(3, 1, 2)
plt.plot(np.abs(signal_after_my_fft))
plt.title("Спектр сигнала (Реализованый БПФ)")
plt.xlabel("Частота")
plt.ylabel("Амплитуда")

plt.subplot(3, 1, 3)
plt.plot(np.abs(signal_after_fft))
plt.title("Спектр сигнала (NumPy БПФ)")
plt.xlabel("Частота")
plt.ylabel("Амплитуда")

plt.tight_layout()
plt.show()
