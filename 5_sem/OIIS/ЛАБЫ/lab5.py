import cv2
import numpy as np

# Загрузка изображений
left = cv2.imread('images_laba5/1.jpg')
right = cv2.imread('images_laba5/2.jpg')

# Изменение порядка каналов с BGR на RGB
left = cv2.cvtColor(left, cv2.COLOR_BGR2RGB)
right = cv2.cvtColor(right, cv2.COLOR_BGR2RGB)

# Выбор метода анаглифа
print("\nВыберите метод анаглифа:")
print("1. True Anaglyphs")
print("2. Gray Anaglyphs")
print("3. Color Anaglyphs")
print("4. Half Color Anaglyphs")
print("5. Optimized Anaglyphs")
print("0. Сохранить все методы")
choice = input("Введите номер метода (0-5): ")

matrices = {
    'true': np.array([[0.299, 0.587, 0.114,
                       0, 0, 0,
                       0, 0, 0],

                      [0, 0, 0,
                       0, 0, 0,
                       0.299, 0.587, 0.114]]),

    'gray': np.array([[0.299, 0.587, 0.114,
                       0, 0, 0,
                       0, 0, 0],

                      [0, 0, 0,
                       0.299, 0.587, 0.114,
                       0.299, 0.587, 0.114]]),

    'color': np.array([[1, 0, 0,
                        0, 0, 0,
                        0, 0, 0],

                       [0, 0, 0,
                        0, 1, 0,
                        0, 0, 1]]),

    'half_color': np.array([[0.299, 0.587, 0.114,
                            0, 0, 0,
                            0, 0, 0],

                           [0, 0, 0,
                            0, 1, 0,
                            0, 0, 1]]),

    'optimized': np.array([[0, 0.7, 0.3,
                            0, 0, 0,
                            0, 0, 0],

                           [0, 0, 0,
                            0, 1, 0,
                            0, 0, 1]]),
}


def make_anaglyph(right, left, color):
    height, width, _ = left.shape
    leftMap = left.copy()
    rightMap = right.copy()
    m = matrices[color]

    for y in range(0, height):
        for x in range(0, width):
            r1, g1, b1 = leftMap[y, x]
            r2, g2, b2 = rightMap[y, x]
            leftMap[y, x] = (
                int(r1 * m[0][0] + g1 * m[0][1] + b1 * m[0][2] + r2 * m[1][0] + g2 * m[1][1] + b2 * m[1][2]),  # r
                int(r1 * m[0][3] + g1 * m[0][4] + b1 * m[0][5] + r2 * m[1][3] + g2 * m[1][4] + b2 * m[1][5]),  # g
                int(r1 * m[0][6] + g1 * m[0][7] + b1 * m[0][8] + r2 * m[1][6] + g2 * m[1][7] + b2 * m[1][8])  # b
            )
    return leftMap

# Применение выбранного метода анаглифа
if choice == '1':
    # True Anaglyphs
    anaglyphed_true = make_anaglyph(left, right, 'true')
    cv2.imwrite('images_laba5/true_anaglyphs.jpg', anaglyphed_true)

elif choice == '2':
    # Gray Anaglyphs
    anaglyphed_gray = make_anaglyph(left, right, 'gray')
    cv2.imwrite('images_laba5/gray_anaglyphs.jpg', anaglyphed_gray)

elif choice == '3':
    # Color Anaglyphs
    anaglyphed_color = make_anaglyph(left, right, 'color')
    cv2.imwrite('images_laba5/color_anaglyphs.jpg', anaglyphed_color)

elif choice == '4':
    # Half-Color Anaglyphs
    anaglyphed_half_color = make_anaglyph(left, right, 'half_color')
    cv2.imwrite('images_laba5/half_color_anaglyphs.jpg', anaglyphed_half_color)

elif choice == '5':
    # Optimized Anaglyphs
    anaglyphed_optimized = make_anaglyph(left, right, 'optimized')
    cv2.imwrite('images_laba5/optimized_anaglyphs.jpg', anaglyphed_optimized)

elif choice == '0':
    anaglyphed_true = make_anaglyph(left, right, 'true')
    anaglyphed_gray = make_anaglyph(left, right, 'gray')
    anaglyphed_color = make_anaglyph(left, right, 'color')
    anaglyphed_half_color = make_anaglyph(left, right, 'half_color')
    anaglyphed_optimized = make_anaglyph(left, right, 'optimized')

    cv2.imwrite('images_laba5/true_anaglyphs.jpg', anaglyphed_true)
    cv2.imwrite('images_laba5/gray_anaglyphs.jpg', anaglyphed_gray)
    cv2.imwrite('images_laba5/color_anaglyphs.jpg', anaglyphed_color)
    cv2.imwrite('images_laba5/half_color_anaglyphs.jpg', anaglyphed_half_color)
    cv2.imwrite('images_laba5/optimized_anaglyphs.jpg', anaglyphed_optimized)

    print('Все 5 результатов анаглифных методов сохранены в папке images_laba5.')
else:
    print("Неверный ввод")
    exit()
