import math
from random import randint

from PIL import Image
from PIL.PyAccess import PyAccess


def apply_threshold(value):
    return 255 * math.floor(value / 128)


def fixed_thresholding(source: str, result: str) -> None:
    image = Image.open(source)
    for x in range(image.width):
        for y in range(image.height):
            threshold = sum(image.getpixel((x, y))[0: 3]) // 3
            color = (255, 255, 255) if threshold > 128 else (0, 0, 0)
            image.putpixel((x, y), color)
    image.save(result)


def random_thresholding(source: str, result: str) -> None:
    image = Image.open(source)
    for x in range(image.width):
        for y in range(image.height):
            threshold = sum(image.getpixel((x, y))[0: 3]) // 3
            color = (255, 255, 255) if threshold > randint(0, 255) else (0, 0, 0)
            image.putpixel((x, y), color)
    image.save(result)


def ordered_dither(source: str, result: str) -> None:
    m = [
        [0, 2],
        [3, 1]
    ]
    image = Image.open(source)
    for x in range(image.width):
        for y in range(image.height):
            threshold = sum(image.getpixel((x, y))[0: 3]) // 3
            color = (255, 255, 255) if threshold * 5 // 256 > m[x % 2][y % 2] else (0, 0, 0)
            image.putpixel((x, y), color)
    image.save(result)


def floyd_steinberg(source: str, output: str):
    """
    Псевдокод взят с https://en.wikipedia.org/wiki/Floyd–Steinberg_dithering
    """

    new_image = Image.open(source)

    new_image = new_image.convert('L').convert('1').convert('RGB')
    image: PyAccess = new_image.load()

    x_size, y_size = new_image.size

    for y in range(1, y_size):
        for x in range(1, x_size):
            red_oldpixel, green_oldpixel, blue_oldpixel = image[x, y]

            red_newpixel = apply_threshold(red_oldpixel)
            green_newpixel = apply_threshold(green_oldpixel)
            blue_newpixel = apply_threshold(blue_oldpixel)

            image[x, y] = red_newpixel, green_newpixel, blue_newpixel

            red_error = red_oldpixel - red_newpixel
            blue_error = blue_oldpixel - blue_newpixel
            green_error = green_oldpixel - green_newpixel

            if x < x_size - 1:
                red = image[x + 1, y][0] + round(red_error * 7 / 16)
                green = image[x + 1, y][1] + round(green_error * 7 / 16)
                blue = image[x + 1, y][2] + round(blue_error * 7 / 16)

                image[x + 1, y] = (red, green, blue)

            if x > 1 and y < y_size - 1:
                red = image[x - 1, y + 1][0] + round(red_error * 3 / 16)
                green = image[x - 1, y + 1][1] + round(green_error * 3 / 16)
                blue = image[x - 1, y + 1][2] + round(blue_error * 3 / 16)

                image[x - 1, y + 1] = (red, green, blue)

            if y < y_size - 1:
                red = image[x, y + 1][0] + round(red_error * 5 / 16)
                green = image[x, y + 1][1] + round(green_error * 5 / 16)
                blue = image[x, y + 1][2] + round(blue_error * 5 / 16)

                image[x, y + 1] = (red, green, blue)

            if x < x_size - 1 and y < y_size - 1:
                red = image[x + 1, y + 1][0] + round(red_error * 1 / 16)
                green = image[x + 1, y + 1][1] + round(green_error * 1 / 16)
                blue = image[x + 1, y + 1][2] + round(blue_error * 1 / 16)

                image[x + 1, y + 1] = (red, green, blue)

    new_image.save(output)


def main() -> None:
    fixed_thresholding('source/img.png', 'result/image-0.png')
    random_thresholding('source/img.png', 'result/image-1.png')
    ordered_dither('source/img.png', 'result/image-2.png')
    floyd_steinberg('source/img.png', 'result/image-3.png')


if __name__ == '__main__':
    main()