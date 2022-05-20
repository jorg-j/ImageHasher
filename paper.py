"""
Simple Application to detect for images which are predominantly white
"""

from statistics import mean

from PIL import Image


def get_main_color(file):
    """
    It takes an image file, resizes it to 16x16, gets the colors in the image, and returns the most
    common color and the percentage of the image that color takes up

    :param file: The path to the image file
    :return: The most present color in the image and the percentage of the image that is that color.
    """
    img = Image.open(file).resize((16, 16))
    colors = img.getcolors(
        maxcolors=256
    )  # put a higher value if there are many colors in your image

    max_occurence, most_present = 0, 0
    try:
        for c in colors:
            if c[0] > max_occurence:
                (max_occurence, most_present) = c
        percent = max_occurence / len(colors) * 100
        return most_present, percent
    except TypeError:
        raise Exception("Too many colors in the image")


def _check(value):
    """
    If the value is greater than 240, return True, otherwise return False.

    :param value: The value to be checked
    :return: True or False
    """
    if value > 240:
        return True
    else:
        return False


def check_image(filename):
    """
    It takes an image, finds the most dominant color, and if that color is white, it returns True

    :param filename: The filename of the image you want to check
    :return: a boolean value.
    """

    primary_col, percent = get_main_color(filename)

    if percent > 75:
        try:
            conversion = str(primary_col)
            white = _check(primary_col)
        except:
            averages = mean(list(primary_col))
            white = _check(averages)
        if white:
            return True
        else:
            return False
    else:
        return False


