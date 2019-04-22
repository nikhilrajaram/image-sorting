import tensorflow as tf
import numpy


import dhash
from PIL import Image
import os
import json


def compute_dhash(filename, hash_size = 8):
    #hash size of 8 = 9*9 downscaled image and 8*8 size column/row hash (128 bits total)
    dhash.force_pil()
    image = Image.open(filename)
    row, col = dhash.dhash_row_col(image, size=hash_size)
    return dhash.format_hex(row, col)

def compareImages(file1, file2, hash_size = 8):
    # hamming distance of hashes
    dh1 = int(compute_dhash(file1, hash_size), 16)
    dh2 = int(compute_dhash(file2, hash_size), 16)
    return dhash.get_num_bits_different(dh1, dh2)

def compareHashes(h1, h2):
    h1 = int(h1, 16)
    h2 = int(h2, 16)
    return dhash.get_num_bits_different(h1, h2)

def findDuplicates(distance = 10, hash_size = 8):
    folder = "interface/static/PhotoSorter_images/"
    img_names = os.listdir(folder)
    imgs = [folder + file for file in img_names]
    hashes = []
    total = len(imgs)
    for i,v in enumerate(imgs):
        hashes.append(compute_dhash(v, hash_size))
        print(str((i/total)*100) + "%")
    # hashes = [compute_dhash(file, hash_size) for file in imgs]
    hash_dict = dict(zip(img_names, hashes))
    compared = {(img_names[i], img_names[j]): compareHashes(x, y) for i,x in enumerate(hashes) for j,y in enumerate(hashes) if i != j}

    # save to json
    jsonf = json.dumps(compared)
    f = open("imageComparisons.json", "w")
    f.write(jsonf)
    f.close()
    return compared

f = findDuplicates()
print(f)
print(len(f))
