#!/usr/bin/env python
from __future__ import absolute_import, division, print_function

import doctest
from glob import glob
import PIL

import imagehash
import six
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from utils.hashtools import is_image, runhash, cropres

from dbman import Db


def check_hash_match(img, flip):
    """

    Takes the filename of the image, hashes using various methods.
    Checks for hash in db.
    Given hash exists then returns a deduplicated list of possible results.

    >>> check_hash_match(img='/Users/jackjorgensen/Pictures/Albury/Tower.jpeg')
    ['/Users/jackjorgensen/Pictures/Melbourne/IMG_1091.jpeg']

    """
    results = []
    hashes = dict(
        ahash=runhash(img, imagehash.average_hash, flip),
        phash=runhash(img, imagehash.phash, flip),
        dhash=runhash(img, imagehash.dhash, flip),
        whashhaar=runhash(img, imagehash.whash, flip),
        whashdb4=runhash(img, lambda img: imagehash.whash(img, mode="db4"), flip),
        # colorhash=runhash(img, imagehash.colorhash, flip),
        cropresistant=cropres(img, flip),
    )

    for mode, hash in hashes.items():
        if mode == "cropresistant":
            hash_match, filename = db.check_crop_resist(hash=hash, mode=mode)
        else:
            hash_match, filename = db.check_hash(hash=hash, mode=mode)

        if hash_match:
            results.append(filename[0])
    return list(set(results))


def display_side(img, results):
    results.append(img)
    images = [Image.open(x) for x in results]
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_im = Image.new("RGB", (total_width, max_height))

    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0] + 5
    new_im.show()
    


def display_image(img, results):
    original = Image.open(img)
    I1 = ImageDraw.Draw(original)
    myFont = ImageFont.truetype(font=r"C:\Windows\Fonts\arial.ttf", size=65)
    I1.text((200, 300), "Submitted", font=myFont, fill=(255, 0, 0))
    original.show(title=img)
    for i in results:
        im = Image.open(i)
        I1 = ImageDraw.Draw(im)
        I1.text((200, 300), i, font=myFont, fill=(255, 0, 0))
        im.show(title=i)


def find_similar_images(userpath):

    image_filenames = glob(userpath + "*")

    for img in sorted(image_filenames):
        if is_image(img):
            existing = db.check_exist(img)

            if existing == True:
                print("Filename already exists in database")
            else:
                print(f"Checking {img}")
                results = check_hash_match(img, False)
                if len(results) > 0:
                    display_side(img, results)
                else:
                    imgflip = check_hash_match(img, True)
                    if len(imgflip) > 0:
                        display_side(img, imgflip)


# doctest.testmod()

if __name__ == "__main__":
    import sys
    import os
    import configparser

    global db

    config = configparser.ConfigParser()
    config.read("config.ini")
    config_version = "SA"

    db_location = config[config_version]["db"]
    source = config[config_version]["lookup"]

    db = Db(db_location)

    find_similar_images(userpath=source)
