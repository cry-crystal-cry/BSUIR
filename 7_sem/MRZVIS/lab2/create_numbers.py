from PIL import Image, ImageDraw, ImageFont
import os
import numpy as np

folder = "patterns_digits"
os.makedirs(folder, exist_ok=True)
size = (28, 28)

# Шрифт
try:
    font = ImageFont.truetype("arial.ttf", 24)
except:
    font = ImageFont.load_default()

for digit in range(10):  # Цифры от 0 до 9
    char = str(digit)

    # Белый фон
    img = Image.new('L', size, 0)
    draw = ImageDraw.Draw(img)

    bbox = draw.textbbox((0, 0), char, font=font)
    w, h = bbox[2]-bbox[0], bbox[3]-bbox[1]
    pos = ((size[0]-w)//2 - bbox[0], (size[1]-h)//2 - bbox[1])
    draw.text(pos, char, fill=255, font=font)

    # Преобразуем в бинарное: 1/-1 для сети
    arr = np.array(img)
    binary = np.where(arr > 127, 1, -1)

    # Сохраняем бинарный PNG (0 и 255)
    bin_img = ((binary + 1)//2 * 255).astype(np.uint8)
    Image.fromarray(bin_img).save(os.path.join(folder, f"digit_{digit}_bin.png"))


print("Готово! Все цифры 0-9 сохранены как бинарные PNG")
