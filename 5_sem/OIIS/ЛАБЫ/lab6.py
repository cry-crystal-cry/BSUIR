from imageai.Detection import ObjectDetection
from PIL import Image
import os

# Укажите пути к папкам и изображению мяча
exec_path = os.getcwd()
input_folder = 'images_laba6'
output_folder = 'images_result_laba6'
image_path = 'basketball.png'  # Путь к изображению мяча

# Инициализация классификатор

detector = ObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath(os.path.join(exec_path, "retinanet_resnet50_fpn_coco-eeacb38b.pth"))
detector.loadModel()

# Получите список файлов в папке

input_images = os.listdir(input_folder)

# Открываем изображение мяча и сохраняем его в переменной
with Image.open(image_path) as image:
    image = image.convert("RGBA")  # Конвертируем в RGBA

    # Обработка каждого изображения в папке
    for image_file in input_images:
        # Полный путь к изображению
        input_image_path = os.path.join(input_folder, image_file)
        output_image_path = os.path.join(output_folder, f"new_{image_file}")

        # Проверка на то, что файл является изображением
        if image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
            # Выполнение детекции объектов
            detected_objects = detector.detectObjectsFromImage(
                input_image=input_image_path,
                output_image_path=None,  # Устанавливаем None, так как заменяем вручную
                minimum_percentage_probability=90,
                display_percentage_probability=False,
                display_object_name=False
            )

            # Загружаем входное изображение
            with Image.open(input_image_path) as img:
                img = img.convert("RGBA")  # Конвертируем входное изображение в RGBA

                # Обрабатываем находки
                for obj in detected_objects:
                    if obj["name"] == "sports ball":
                        # Получаем координаты Bounding Box мяча
                        x1, y1, x2, y2 = (int(obj["box_points"][0]), int(obj["box_points"][1]),
                                          int(obj["box_points"][2]), int(obj["box_points"][3]))

                        # Вычисляем новое разрешение с увеличением на 15%
                        new_width = int((x2 - x1) * 1.25)  # Увеличиваем ширину на 25%
                        new_height = int((y2 - y1) * 1.25)  # Увеличиваем высоту на 25%

                        # Изменяем размер мяча
                        basketball_resized = image.resize((new_width, new_height))

                        # Вычисляем новое смещение для вставки мяча, чтобы он оставался центрированным
                        new_x1 = x1 - int((new_width - (x2 - x1)) / 2)
                        new_y1 = y1 - int((new_height - (y2 - y1)) / 2)

                        # Накладываем мяч
                        img.paste(basketball_resized, (new_x1, new_y1), basketball_resized)

                # Сохраняем результат
                img.save(output_image_path, format="PNG")  # Сохраняем в PNG для сохранения альфа-канала

print("Обработка завершена!")
