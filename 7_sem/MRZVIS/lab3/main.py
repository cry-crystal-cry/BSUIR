import numpy as np
from model import LSTMModel
from utils import generate_data, create_sequences, Scaler

CONFIG = {
    "common": {
        "seq_len": 35,
        "in_size": 3,
        "out_size": 1,
        "predict_steps": 1,
        "precision": 4,
        "alpha": 0.02,
        "seed": 42
    },
    "tasks": [
        {
            "name": "Геометрическая прогрессия",
            "type": "geometric",
            "epochs": 8000,
            "lr": 0.02,
            "hidden": 32,
            "log": True
        },
        {
            "name": "Числа Фибоначчи",
            "type": "fibonacci",
            "epochs": 8000,
            "lr": 0.02,
            "hidden": 32,
            "log": True
        },
        {
            "name": "Степенная функция (x^2)",
            "type": "power",
            "epochs": 6000,
            "lr": 0.01,
            "hidden": 24,
            "log": False
        },
        {
            "name": "Периодический ряд (Sin)",
            "type": "periodic",
            "epochs": 6000,
            "lr": 0.01,
            "hidden": 24,
            "log": False
        }
    ]
}


def display_params(task, c):
    print(f"\n" + "=" * 95)
    print(f"ЗАДАЧА: {task['name']}")
    print(f"ГИПЕРПАРАМЕТРЫ:")
    print(f" - Общая длина последовательности: {c['seq_len']}")
    print(f" - Размер окна (in_size): {c['in_size']}")
    print(f" - Скрытых нейронов (hidden): {task['hidden']}")
    print(f" - Коэффициент обучения (lr): {task['lr']}")
    print(f" - Количество эпох: {task['epochs']}")
    print(f" - Коэффициент Leaky ReLU (alpha): {c['alpha']}")
    print("=" * 95)


def run_task(task, c):
    np.random.seed(c['seed'])
    display_params(task, c)

    # Генерация данных
    raw_data = generate_data(task['type'], length=c['seq_len'] + 5)
    scaler = Scaler(use_log=task.get('log', False))
    data_norm = scaler.fit_transform(raw_data)

    # Создание последовательностей
    X, y = create_sequences(data_norm, c['in_size'])

    # Отображение обучающей выборки (первые 5 примеров)
    print(f"\nОБУЧАЮЩАЯ ВЫБОРКА (первые 5 образов):")
    print(f"{'Вход (X)':<45} | {'Цель (y)':<15}")
    print("-" * 65)

    is_periodic = (task['type'] == "periodic")

    for i in range(min(5, len(X))):
        x_raw = scaler.inverse_transform(X[i])
        y_raw = scaler.inverse_transform(y[i])

        if is_periodic:
            x_str = "[" + ", ".join([f"{float(v):.4f}" for v in x_raw]) + "]"
            y_str = f"{float(y_raw):.4f}"
        else:
            x_str = str([int(round(float(v))) for v in x_raw])
            y_str = str(int(round(float(y_raw))))

        print(f"{x_str:<45} | {y_str:<15}")

    # Инициализация и обучение
    model = LSTMModel(c['in_size'], task['hidden'], c['out_size'], c['alpha'])
    print(f"\nОбучение...")
    for epoch in range(task['epochs']):
        idx_shuffle = np.random.permutation(len(X))
        for i in idx_shuffle:
            model.train_step(X[i], y[i], task['lr'])

    # Тестирование и вывод результатов
    print(f"\nРЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:")
    print(f"{'Входные значения':<35} | {'Ожидаемо':<20} | {'Предсказано (float)':<30}")
    print("-" * 95)

    indices = [0, len(X) // 2, len(X) - 1]
    for idx in indices:
        x_sample_norm = X[idx]
        y_true_real = raw_data[idx + c['in_size']: idx + c['in_size'] + c['predict_steps']]

        curr_window = list(x_sample_norm)
        preds_norm = []
        for _ in range(c['predict_steps']):
            p_n, _ = model.forward(np.array(curr_window))
            val = p_n[0, 0]
            preds_norm.append(val)
            curr_window.append(val)
            curr_window.pop(0)

        # Логика отображения (Periodic = float, Остальные = int)
        if is_periodic:
            x_real = [round(float(v), 4) for v in scaler.inverse_transform(x_sample_norm)]
            y_real = [round(float(v), 4) for v in y_true_real]
        else:
            x_real = [int(round(float(v))) for v in scaler.inverse_transform(x_sample_norm)]
            y_real = [int(round(float(v))) for v in y_true_real]

        p_real = scaler.inverse_transform(np.array(preds_norm))

        x_disp = f"{x_real}"
        y_disp = f"{y_real}"
        p_disp = ", ".join([f"{v:.{c['precision']}f}" for v in p_real])

        print(f"{x_disp:<35} | {y_disp:<20} | {p_disp:<30}")


if __name__ == "__main__":
    for task in CONFIG['tasks']:
        run_task(task, CONFIG['common'])
