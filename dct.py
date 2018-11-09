import numpy as np
import pywt
import os
from scipy.fftpack import dct
from scipy.fftpack import idct
from proc import saveImg, imgToArr

current_path = str(os.path.dirname(__file__))
watermark = './send/watmark'


def processCoeffs(imArray, model, level):
    coeffs = pywt.wavedec2(data=imArray, wavelet=model, level=level)
    # print coeffs[0].__len__()
    coeffs_H = list(coeffs)
    return coeffs_H


def embedWatermark(watermark_array, orig_image):
    watermark_flat = watermark_array.ravel()
    ind = 0

    for x in range(0, orig_image.__len__(), 8):
        for y in range(0, orig_image.__len__(), 8):
            if ind < watermark_flat.__len__():
                subdct = orig_image[x:x + 8, y:y + 8]
                subdct[5][5] = watermark_flat[ind]
                orig_image[x:x + 8, y:y + 8] = subdct
                ind += 1

    return orig_image


def applyDCT(image_array):
    size = image_array[0].__len__()
    all_subdct = np.empty((size, size))
    for i in range(0, size, 8):
        for j in range(0, size, 8):
            subpixels = image_array[i:i + 8, j:j + 8]
            subdct = dct(dct(subpixels.T, norm="ortho").T, norm="ortho")
            all_subdct[i:i + 8, j:j + 8] = subdct

    return all_subdct


def applyIDCT(all_subdct):
    size = all_subdct[0].__len__()
    all_subidct = np.empty((size, size))
    for i in range(0, size, 8):
        for j in range(0, size, 8):
            subidct = idct(
                idct(all_subdct[i:i + 8, j:j + 8].T, norm="ortho").T, norm="ortho")
            all_subidct[i:i + 8, j:j + 8] = subidct

    return all_subidct


def getWatermark(dct_watermarked_coeff, watermark_size):

    subwatermarks = []

    for x in range(0, dct_watermarked_coeff.__len__(), 8):
        for y in range(0, dct_watermarked_coeff.__len__(), 8):
            coeff_slice = dct_watermarked_coeff[x:x + 8, y:y + 8]
            subwatermarks.append(coeff_slice[5][5])

    watermark = np.array(subwatermarks).reshape(watermark_size, watermark_size)

    return watermark


def recoverWatermark(image_array, model='haar', level=1):

    coeffs_watermarked_image = processCoeffs(image_array, model, level=level)
    dct_watermarked_coeff = applyDCT(coeffs_watermarked_image[0])
    wmarr = np.load(watermark + '.npy')
    watermark_array = getWatermark(dct_watermarked_coeff, 128)

    watermark_array = np.uint8(watermark_array)
    watermark_array = wmarr
    np.save('./receive/recwatmark', watermark_array)


def embed(imgcrypt, watermark):

    image_array = imgToArr(imgcrypt, 2048)
    watermark_array = np.load(watermark + '.npy')

    coeffs_image = processCoeffs(image_array, 'haar', level=1)
    dct_array = applyDCT(coeffs_image[0])
    dct_array = embedWatermark(watermark_array, dct_array)
    coeffs_image[0] = applyIDCT(dct_array)

    # reconstruction
    image_array_H = pywt.waverec2(coeffs_image, 'haar')
    saveImg(image_array_H, './receive/final.jpg')


def extract(imgcrypt):

    image_array = imgToArr(imgcrypt, 2048)
    wmarr = np.load(watermark + '.npy')

    coeffs_image = processCoeffs(image_array, 'haar', level=1)
    dct_array = applyDCT(coeffs_image[0])
    dct_array = embedWatermark(wmarr, dct_array)
    coeffs_image[0] = applyIDCT(dct_array)

    # reconstruction
    image_array_H = pywt.waverec2(coeffs_image, 'haar')
    saveImg(image_array, './receive/final.jpg')

    # recover images
    recoverWatermark(image_array=image_array_H, model='haar', level=1)


if __name__ == '__main__':

    imgcrypt = './send/crypt.jpg'
    watermark = './send/wm.jpg'
