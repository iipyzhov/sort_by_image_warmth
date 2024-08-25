import os #для работы с файлами
from PIL import Image #для обработки изображения
import webbrowser #для открытия готовой HTML страницы в браузере


def get_weighted_warmth_score(image):
    max_distance = 390 #максимальное расстояние до центра теплоты на цветовом круге
    target_hue = 30  #оттенок максимальной теплоты цвета на цветовом круге

    total_weight = 0
    total_pixels = 0

    #открываем изображение с использованием Pillow
    image_pil = Image.open(image)

    #считается кол-во пикселей с "теплыми" оттенками и определяется его отношение к общему кол-ву пикселей -- степень теплоты изображения
    for pixel in image_pil.getdata():
        r, g, b = pixel #для каждого пикселя извлекаются значения красного, зеленого и синего цветов
        #проверка, не является ли цвет нейтральным
        if r == g == b:
            continue

        hue = get_hue(pixel)
        distance = min(abs(hue -  target_hue), max_distance - abs(hue -  target_hue))

        # Определение веса для пикселя на основе удаленности от  цвета максимальной теплоты
        # Чем ближе к нему, тем больший вес
        weight = 1.0 - (distance / max_distance)

        # Если пиксель теплый и не нейтральный
        if is_warm_color(pixel):
            total_weight += weight
        total_pixels += 1

    return total_weight / total_pixels

#для определения теплоты изображения используется анализ цветовых пикселей изображения в цветовой модели HSL.
#задается диапазон теплых цветов. Теплыми считаем оттенки в диапазоне [0, 120) и [300, 360) на цветовом круге
def is_warm_color(color):
    hue = get_hue(color)
    return (0 <= hue <= 120) or (300 <= hue < 360)

#Изображение преобразуется из цветовой модели RGB (Red, Green, Blue) в HSL
#определяется оттенок(Hue) каждого пикселя в цвет. модели HSL. На основе оттенка(измеряется в градусах) определяем цвет пикселя на цветовом круге, соответственно, теплоту цвета
def get_hue(rgb_color):
    r, g, b = rgb_color
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    max_color = max(r, g, b)
    min_color = min(r, g, b)

    if max_color == min_color:
        hue = 0
    elif max_color == r:
        hue = (60 * ((g - b) / (max_color - min_color)) + 360) % 360
    elif max_color == g:
        hue = 60 * ((b - r) / (max_color - min_color)) + 120
    else:
        hue = 60 * ((r - g) / (max_color - min_color)) + 240

    return hue

#Изображения с высоким уровнем теплых цветов (отношение теплых к общему >=50%) собираются и выводятся на HTML-страницу.
#функция, которая создает сетку изображений на основе уровня теплоты, просматривает файлы в указанной папке и вычисляет "теплоту" каждого изображения, если уровень теплоты больше или равен 0.5 (50%), изображение добавляется в список images.
def create_image_grid(image_folder):
    images = []
    for filename in os.listdir(image_folder):
        if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            image_path = os.path.join(image_folder, filename)
            warmth_score = get_weighted_warmth_score(image_path)
            #фильтруются изображения, за исключением тех, на которых преобладают холодные цвета( >50%)
            if warmth_score >= 0.5:
                images.append((image_path, warmth_score))

    # сортировка по убыванию уровня теплых цветов
    images.sort(key=lambda x: x[1], reverse=True)
    # генерация HTML страницы
    with open('output.html', 'w') as f:
        f.write('''<!DOCTYPE html>
<html>
<head>
    <title>Изображения с теплыми цветами</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            background-color: #f7f7f7;
            margin: 0;
            padding: 0;
        }

        h1 {
            color: #333;
            font-size: 36px;
            margin-top: 20px;
        }

        .image-grid {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 20px;
            max-width: 100%;
            margin: 0 auto;
        }

        .image {
            border: 1px solid #ddd;
            background-color: #fff;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
            border-radius: 10px;
            padding: 20px;
        }

        img {
            max-width: 100%;
            height: auto;
            border-radius: 10px;
        }

        .percentage {
            font-size: 24px;
            margin-top: 10px;
            color: #777;
        }
    </style>
</head>
<body>
    <h1>Изображения с теплыми цветами</h1>
    <div class="image-grid">
    ''')
        for image_path, warmth_score in images:
            f.write(f'''
            <div class="image">
                <img src="{image_path}" alt="Image">
                <p class="percentage">Теплота: {warmth_score:.2%}</p>
            </div>
            ''')
        f.write('</div></body></html>')

#путь к папке с изображениями "images", находящейся в той же директории, что и скрипт
#используется относительный путь(относительно расположения скрипта, а не жестко закодированный путь к файлу
image_folder = os.path.join(os.path.dirname(__file__), 'images')

#создание HTML страницы и открытие в браузере
create_image_grid(image_folder)
webbrowser.open('output.html')
#"теплота" изображения определяется на основе его цветовой палитры и соответствия оттенков в цветовой модели HSL определенному диапазону, который считается "теплым"