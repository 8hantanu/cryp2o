import numpy as np
from copy import deepcopy
from proc import keyToInt


def lfsr(key, locs, imgdim):

    seed = keyToInt(key)
    imgsize = imgdim[0] * imgdim[1]
    lfsrkey = deepcopy(seed)

    while len(lfsrkey) <= imgsize:
        nextbit = 0
        for loc in locs:
            nextbit = nextbit ^ lfsrkey[len(lfsrkey)-len(seed) + loc]
        lfsrkey.append(nextbit % 255)

    lfsrkey = np.array(lfsrkey)
    lfsrkey = np.resize(lfsrkey, (imgdim[0], imgdim[1]))
    return lfsrkey


def streamCrypt(keyarr, imgarr, encrypt=True):

    if encrypt:
        imgcrypt = imgarr + keyarr
    else:
        imgcrypt = imgarr - keyarr
    imgcrypt = imgcrypt % 255
    return imgcrypt
