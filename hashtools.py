from __future__ import absolute_import, division, print_function

import imagehash
import six
from PIL import Image

import dbman


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
    """
    It takes an image, and if the flip parameter is set to True, it flips the image horizontally, then
    it calculates the hash of the image
    
    :param img: the image file to be hashed
    :param flip: if True, the image is flipped left to right before hashing, defaults to False
    (optional)
    :return: The hash is being returned.
    """

    # minseg = 10, segmentation size = 600
    try:
        if flip:
            im = Image.open(img)
            
            hash = imagehash.crop_resistant_hash(image=im.transpose(Image.FLIP_LEFT_RIGHT),min_segment_size=500, segmentation_image_size=300, hash_func=imagehash.phash)
        else:
            hash = imagehash.crop_resistant_hash(image=Image.open(img),min_segment_size=500, segmentation_image_size=300, hash_func=imagehash.phash)

    except Exception as e:
        print('Problem:', e, 'with', img)
        hash = ""
    return hash


def is_image(filename):
    """
    If the filename ends with any of the following extensions, return True: .png, .jpg, .jpeg, .bmp,
    .gif, .svg. 
    
    If the filename contains the string ".jpg", return True. 
    
    Otherwise, return False.
    
    :param filename: The name of the file to be uploaded
    :return: A list of all the files in the directory
    """
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
