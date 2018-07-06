import numpy as np
import cv2
from pyldpc import ldpc_images

# Interlacing has been implemented with the adam7 algorithm,
# as recommended for the png file format.

# Each channel has been implemented with the interlacing algorithm in mind.
# Dude to the 7 step algorithm of interlacing, data had to be disrupted at each stage of transmission.


def bsc_noise(x, y):
    it = 0
    it2 = 0
    x_iterator = 8
    y_iterator = 8
    counter = 1
    p = 0.01
    while counter <= 7:
        while it < len(y):
            while it2 < len(y[it]):
                if (y[it][it2] != x[it][it2]).any():
                    y[it][it2] = x[it][it2]
                    y[it][it2] ^= np.random.random((len(y[it][it2]),)) < p
                it2 += x_iterator
            it2 = 0
            it += y_iterator
        counter += 1
        it = 0
        if counter % 2 == 0:
            x_iterator = x_iterator // 2
        else:
            y_iterator = y_iterator // 2
    return y


def gilbert_noise(x, y):

    p_bg = 0.01
    p_gb = 0.001

    it = 0
    it2 = 0
    x_iterator = 8
    y_iterator = 8
    counter = 1
    current_state = 'G'
    while counter <= 7:
        while it < len(y):
            while it2 < len(y[it]):
                if (y[it][it2] != x[it][it2]).any():
                    for it3 in range(0, len(y[it][it2])):
                        if current_state == 'G':
                            if np.random.random() < p_gb:  # symulacja zmiany stanu z prawdopodobienstwiem pDZ
                                current_state = 'B'  # zmiana stanu
                            y[it][it2][it3] = x[it][it2][it3]
                        elif current_state == 'B':
                            if np.random.random() < p_bg:
                                current_state = 'G'
                            y[it][it2][it3] = 1 - x[it][it2][it3]
                it2 += x_iterator
            it2 = 0
            current_state = 'G'
            it += y_iterator
        counter += 1
        it = 0
        if counter % 2 == 0:
            x_iterator = x_iterator // 2
        else:
            y_iterator = y_iterator // 2
    return y


image = cv2.imread("inFile.png", 1)
image_arr = ldpc_images.RGB2Bin(image)
hamming_arr = np.zeros_like(image_arr)

# hamming_arr = bsc_noise(image_arr, hamming_arr)
hamming_arr = gilbert_noise(image_arr, hamming_arr)

image_final = ldpc_images.Bin2RGB(hamming_arr)
cv2.imwrite("outFileITL.png", image_final)
