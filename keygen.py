from Crypto.PublicKey import RSA
from bitarray import bitarray

def keysRSA():
    key = RSA.generate(2048)
    with open("./key/private.key", 'w') as keyFile:
        keyFile.write((key.exportKey()).decode())
    pubkey = key.publickey()
    with open("./key/public.key", 'w') as keyFile:
        keyFile.write((pubkey.exportKey()).decode())


def assignkeys():

    privS = RSA.importKey(open("./keyS/private.key", "rb"))
    privR = RSA.importKey(open("./keyR/private.key", "rb"))
    pubS = privS.publickey()
    pubR = privR.publickey()

    return privS, privR, pubS, pubR


def LSFR(seed, locs, imgsize):

    lsfrkey = seed
    while len(lsfrkey) < imgsize:
        nextbit = 1
        for loc in locs:
            nextbit = nextbit ^ lsfrkey[len(lsfrkey)-len(seed) + loc]
        lsfrkey.append(nextbit)

    return lsfrkey


if __name__ == '__main__':

    lfsr('absfasdd', (8,7,6,1), 10000)
