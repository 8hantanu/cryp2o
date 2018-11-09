import matplotlib.pyplot as plt
import numpy as np
from rsa import assignkeys, messageEncrypt, messageDecrypt
from stream import streamCrypt, lfsr
from proc import keyToInt, intToKey, saveImg, imgToArr, removeFile
from scipy.fftpack import rfft, irfft
from dct import embed, extract


def send():

    # Keys required
    privS, _, _, pubR = assignkeys()

    print('Encrypting ...')
    # imgfile = raw_input("Enter image file path: ")
    imgfile = './send/img.jpg'
    sckey = raw_input("Enter stream cipher key: ")
    imgarr = imgToArr(imgfile, 2048)

    # Generate the stream cipher key through LFSR
    keyarr = lfsr(sckey, [2, 3, 5, 6],  imgarr.shape)

    # Get FFT of image
    fftarr = rfft(rfft(imgarr, axis=0), axis=1)
    saveImg(fftarr, './send/fft.jpg')

    # Encrypt fft of image with LFSR key using stream cipher
    imcarr = streamCrypt(keyarr, fftarr, True)

    # Encrypting stream cipher key into a watermark
    KI = messageEncrypt(sckey, pubR)
    # Authentication using private key of sender
    KII = messageDecrypt(KI, privS)
    KIIint = keyToInt(KII)
    KIIint = np.array(KIIint)
    crykey = np.resize(KIIint, (128, 128))

    # Embedding watermark into image
    imgcrypt = './send/crypt.jpg'
    watermark = './send/watmark'
    saveImg(imcarr, imgcrypt)
    np.save(watermark, crykey)
    embed(imgcrypt, watermark)

    print('... finished encryption')


def receive():

    # Keys required
    _, privR, pubS, _ = assignkeys()

    print('Decrypting ...')
    # rimfile = raw_input("Enter image file path: ")
    rimfile = './receive/final.jpg'
    # Extract watemark(stream cypher key) and extract image
    extract(rimfile)

    # Decrypt watermark using RSA keys
    recoveredWatermark = './receive/recwatmark'
    rimarr = imgToArr(rimfile, 2048)
    ciparr = np.load(recoveredWatermark + '.npy')
    dKII = intToKey(ciparr)

    # Authentication verified
    dKI = messageEncrypt(dKII, pubS)

    # Decrypt rsa key to obtain stream cipher key
    dKey = messageDecrypt(dKI, privR)
    print('The key used for steam cipher decryption is ' + dKey)

    # Decrypting image in frequency domain using stream cipher
    keyarr = lfsr(dKey, [2, 3, 5, 6],  rimarr.shape)
    imcarr = streamCrypt(keyarr, rimarr, False)
    imcarr = rfft(rfft(rfftar, axis=0), axis=1)
    imcarr = irfft(irfft(imcarr, axis=1), axis=0)
    imgdecrypt = './receive/dfft.jpg'
    saveImg(imcarr, imgdecrypt)

    # Transforming back from frequency domain using IFFT
    imgrec = irfft(irfft(imcarr, axis=1), axis=0)
    imgorig = './receive/orig.jpg'
    saveImg(imgrec, imgorig)

    print('... finished decryption')


def clean():
    files = ['./send/fft.jpg', './send/crypt.jpg', './send/watmark.npy', './receive/final.jpg', './receive/dfft.jpg', './receive/orig.jpg', './receive/recwatmark.npy', '.*.pyc']
    for file in files:
        removeFile(file)


imgfile = './send/img.jpg'
imgarr = plt.imread(imgfile).astype(float)
rfftar = rfft(rfft(imgarr, axis=0), axis=1)


if __name__ == '__main__':

    option = int(raw_input("Enter number\n1 for encrypting \n2 for decrypting\n3 for removing files\n"))
    if option == 1:
        send()
    elif option == 2:
        receive()
    elif option == 3:
        clean()
    else:
        pass
