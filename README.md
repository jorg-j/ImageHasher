#!/usr/bin/env python
from __future__ import absolute_import, division, print_function

import imagehash
import six
from PIL import Image
import datetime
import configparser
from multiprocessing import Pool, Semaphore, cpu_count

from dbman import Db
from utils.hashtools import runhash, is_image, cropres


# It takes an image, hashes it, and adds it to the database
class ImageData:
    def __init__(self, img):
        db_location, _ = fetch_config(version='SA')
        self.db = Db(db_location)
        self.mode = "init"
        self.exists = self.db.check_exist(img)
        self.img = img
        self.hashed = False

    def hash_img(self):
        """
        It takes an image, runs it through a series of image hashing functions, and returns the results
        """
        self.ahash = runhash(self.img, imagehash.average_hash)
        self.phash = runhash(self.img, imagehash.phash)
        self.dhash = runhash(self.img, imagehash.dhash)
        self.haar = runhash(self.img, imagehash.whash)
        self.db4 = runhash(self.img, lambda img: imagehash.whash(img, mode="db4"))
        self.color = runhash(self.img, imagehash.colorhash)
        self.crop = cropres(self.img)
        if str(self.ahash) != "":
            self.hashed = True
    
    def add_to_db(self):
        """
        It takes the image, and then it hashes it using the following methods: ahash, phash, dhash, haar,
        db4, color, and crop
        """

        self.db.add_hash(
            filename=self.img,
            ahash=self.ahash,
            phash=self.phash,
            dhash=self.dhash,
            haar=self.haar,
            db4=self.db4,
            color=self.color,
            crop=self.crop
        )


def process_image(img):
    """
    It takes an image, checks if it exists in the database, hashes it if it doesn't, and adds it to the
    database if it's been hashed
    
    :param img: The image to be processed
    """
    image = ImageData(img=img)
    if image.exists == False:
        image.hash_img()
        if image.hashed:
            image.add_to_db()


def worker(img):
    """
    It takes an image, checks if it exists in the database, hashes it if it doesn't, and adds it to the
    database if it's been hashed
    
    :param img: The image to be processed
    """

    image = ImageData(img=img)
    if image.exists == False:
        image.hash_img()
        if image.hashed:
            image.add_to_db()

def fetch_config(version, file='config.ini'):
    config = configparser.ConfigParser()
    config.read(file)
    config_version = version

    db_location = config[config_version]["db"]
    source = config[config_version]["source"]
    return db_location, source


if __name__ == "__main__":
    import os
    import sys



    global db
  
    
    db_location, source = fetch_config(version='SA')

    # connect to database
    db = Db(db_location)

    paths = os.listdir(source)
    start = datetime.datetime.now()
    
    fullfiles = []

    for p in paths:
        image_name = os.path.join(source, p)
        fullfiles.append(image_name)
        # try:

            
        #     process_image(img=image_name)
            
        # except Exception as e:
        #     print(e)
    poolsize = Semaphore(cpu_count())
    print(poolsize)
    p = Pool(2)
    p.map(worker, fullfiles)

    print(datetime.datetime.now() - start)
