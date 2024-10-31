
from PIL import Image, ImageDraw

# Указываем размеры изображения
width, height = 200, 200

# Создаем новое изображение белого цвета
image = Image.new("RGB", (width, height), "white")

# Создаем объект для рисования
draw = ImageDraw.Draw(image)

# Рисуем прямоугольник (координаты начала и конца, цвет)
draw.rectangle([(50, 50), (150, 150)], fill="blue", outline="black")

# Сохраняем изображение
image.save("rectangle_image.png")

# Показываем изображение
image.show()
