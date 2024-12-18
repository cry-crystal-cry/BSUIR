import cv2
import os
import numpy as np

# Директория с исходными изображениями
image_dir = 'images_laba5'

# Загрузка исходного изображения
image = cv2.imread(os.path.join(image_dir, '1.jpg'))

# Сдвиг изображения
rows, cols, _ = image.shape
shift_x = 30  # Величина сдвига по горизонтали
M = np.float32([[1, 0, shift_x], [0, 1, 0]])
shifted_image = cv2.warpAffine(image, M, (cols, rows))

# Создание красной маски для заполнения левой части
mask_shift_x = shift_x + 20  # Величина сдвига маски
mask = np.zeros((rows, mask_shift_x, 3), dtype=np.uint8)

# Наложение маски на сдвинутое изображение
result = shifted_image.copy()
result[:, :mask_shift_x] = mask[:, :mask_shift_x]

# Сохранение результата
cv2.imwrite(os.path.join(image_dir, '2.jpg'), result)
