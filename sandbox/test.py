import glob
import os

userpaths = "/media/jack/Backup/WMM/Categories/"




def is_image(filename):
    f = filename.lower()
    return f.endswith(".png") or f.endswith(".jpg") or \
        f.endswith(".jpeg") or f.endswith(".bmp") or \
        f.endswith(".gif") or '.jpg' in f or f.endswith(".svg")

image_filenames = []

paths = os.listdir("/media/jack/Backup/WMM/Categories/")
print(paths)

# for userpath in userpaths:
#     image_filenames += [os.path.join(userpath, path)
#                         for path in os.listdir(userpath) if is_image(path)]
                    
# print(image_filenames)