import os
import numpy as np
from PIL import Image


def keyToInt(key):

    intarr = [len(key)]
    for cha in key:
        intarr.append(ord(cha))

    return intarr


def intToKey(intkey):

    keyarr = ''
    intkey = np.resize(intkey, (1, 128*128))
    intkey = intkey[0]
    for i in range(256):
        keyarr += chr(int(intkey[i+1]))

    return keyarr


def imgToKey(imgfile):

    keyarr = imgToArr(imgfile, 128, type=np.int)
    print keyarr[0]
    key = ''
    for i in range(12):
        key += chr(int(keyarr[0][i]))

    return key


def imgToArr(image_name, size, type=np.int):

    img = Image.open(image_name).resize((size, size), 1)
    img = img.convert('L')
    img.save(image_name)
    image_array = np.array(img.getdata(), dtype=type).reshape((size, size))
    return image_array


def saveImg(image_array, name):

    image_array_copy = image_array.clip(0, 255)
    image_array_copy = image_array_copy.astype("uint8")
    img = Image.fromarray(image_array_copy)
    img.save(name)


def removeFile(filename):
    try:
        os.remove(filename)
    except OSError:
        pass

if __name__ == '__main__':


    key = "BITSF463"
    from rsa import assignkeys, messageEncrypt, messageDecrypt
    privS, privR, pubS, pubR = assignkeys()
    key = messageEncrypt(key, pubR)
    key = messageDecrypt(key, privS)
    intkey = keyToInt(key)
    KIIint = np.array(intkey)
    keyimg = np.resize(KIIint, (128, 128))
    print(keyimg)
    np.save('key', keyimg)
    arr = np.load('key' + '.npy')
    print(arr)
    key = intToKey(arr)
    key = messageEncrypt(key, pubS)
    key = messageDecrypt(key, privR)
    print(key)
