from __future__ import (absolute_import, division, print_function)
from PIL import Image
import six
import dbman
import imagehash


def runhash(img, hashfunc, flip=False):
    '''

    Take filename of image and the hash function and return the result.
    
    >>> runhash(img='~/Pictures/Albury/Tower.jpeg', hashfunc=imagehash.phash)
    array([[ True,  True, False, False,  True,  True,  True, False],
           [False, False, False, False,  True, False, False,  True],
           [False, False,  True,  True, False,  True, False, False],
           [ True,  True,  True,  True, False, False,  True, False],
           [ True, False, False,  True,  True, False,  True,  True],
           [False, False, False, False,  True,  True,  True,  True],
           [ True, False, False,  True, False, False,  True, False],
           [ True,  True, False,  True,  True,  True, False, False]])
    '''
    try:
        if flip:
            im = Image.open(img)
            hash = hashfunc(im.transpose(Image.FLIP_LEFT_RIGHT))
        else:
            hash = hashfunc(Image.open(img))

    except Exception as e:
        print('Problem:', e, 'with', img)
        hash = ""
    return hash

def cropres(img, flip=False):

    try:
        if flip:
            im = Image.open(img)
            hash = imagehash.crop_resistant_hash(image=im.transpose(Image.FLIP_LEFT_RIGHT),min_segment_size=10, segmentation_image_size=600)
        else:
            hash = imagehash.crop_resistant_hash(image=Image.open(img),min_segment_size=10, segmentation_image_size=600)

    except Exception as e:
        print('Problem:', e, 'with', img)
        hash = ""
    return hash


def is_image(filename):
    f = filename.lower()
    return (
        f.endswith(".png")
        or f.endswith(".jpg")
        or f.endswith(".jpeg")
        or f.endswith(".bmp")
        or f.endswith(".gif")
        or ".jpg" in f
        or f.endswith(".svg")
    )