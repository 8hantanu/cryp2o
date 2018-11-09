from Crypto.PublicKey import RSA
from ast import literal_eval
from proc import keyToInt, intToKey


def keysRSA():
    key = RSA.generate(2048)
    with open("./key/private.key", 'w') as keyFile:
        keyFile.write((key.exportKey()).decode())
    pubkey = key.publickey()
    with open("./key/public.key", 'w') as keyFile:
        keyFile.write((pubkey.exportKey()).decode())


def assignkeys():

    privS = RSA.importKey(open("./keyS/private.key", "r"))
    privR = RSA.importKey(open("./keyR/private.key", "r"))
    pubS = privS.publickey()
    pubR = privR.publickey()

    return privS, privR, pubS, pubR


def messageEncrypt(message, key):
    eMessage = key.encrypt(message, 32)
    return eMessage


def messageDecrypt(eMessage, key):
    dMessage = key.decrypt(literal_eval(str(eMessage)))
    return dMessage



if __name__ == '__main__':

    privS, privR, pubS, pubR = assignkeys()

    key = 'Some Random Key'

    KI = messageEncrypt(key, pubR)
    KII = messageDecrypt(KI, privS)

    KIIint = keyToInt(KII)
    print(type(key))
    KIIkey = intToKey(KIIint)
    print(KIIkey == KII)
    dKII = KIIkey


    dKI = messageEncrypt(dKII, pubS)
    dKey = messageDecrypt(KI, privR)
