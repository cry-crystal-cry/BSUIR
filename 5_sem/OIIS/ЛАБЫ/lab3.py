from PIL import Image

# Открываем изображения
img1 = Image.open('images_laba3/1.jpg')
img2 = Image.open('images_laba3/2.jpg')

# Обрабатываем первое изображение
img1_pixels = list(img1.getdata())
img1_mean_brightness = sum(pixel[0] + pixel[1] + pixel[2] for pixel in img1_pixels) / (len(img1_pixels) * 3)

# Обрабатываем второе изображение
img2_pixels = list(img2.getdata())
img2_mean_brightness = sum(pixel[0] + pixel[1] + pixel[2] for pixel in img2_pixels) / (len(img2_pixels) * 3)

# Находим разницу в яркости
brightness_diff = abs(img1_mean_brightness - img2_mean_brightness) / 2

# Уменьшаем/увеличиваем значения яркости изображений

if img1_mean_brightness > img2_mean_brightness:
    new_img1_pixels = [(max(0, int(pixel[0] - brightness_diff)),
                        max(0, int(pixel[1] - brightness_diff)),
                        max(0, int(pixel[2] - brightness_diff))) for pixel in img1_pixels]

    new_img2_pixels = [(min(255, int(pixel[0] + brightness_diff)),
                        min(255, int(pixel[1] + brightness_diff)),
                        min(255, int(pixel[2] + brightness_diff))) for pixel in img2_pixels]
else:
    new_img1_pixels = [(min(255, int(pixel[0] + brightness_diff)),
                        min(255, int(pixel[1] + brightness_diff)),
                        min(255, int(pixel[2] + brightness_diff))) for pixel in img1_pixels]

    new_img2_pixels = [(max(0, int(pixel[0] - brightness_diff)),
                        max(0, int(pixel[1] - brightness_diff)),
                        max(0, int(pixel[2] - brightness_diff))) for pixel in img2_pixels]


# Получаем размеры изображений
img1_width, img1_height = img1.size
img2_width, img2_height = img2.size

# Создаем новые изображения
new_img1 = Image.new('RGB', (img1_width, img1_height))
new_img1.putdata(new_img1_pixels)
new_img2 = Image.new('RGB', (img2_width, img2_height))
new_img2.putdata(new_img2_pixels)

# Сохраняем новые изображения
new_img1.save('images_laba3/result_1.jpg')
new_img2.save('images_laba3/result_2.jpg')
