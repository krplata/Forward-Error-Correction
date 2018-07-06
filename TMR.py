import numpy as np
import cv2
from pyldpc import ldpc_images

p = 0.01
image = cv2.imread("inFile.png", 1)
x = ldpc_images.RGB2Bin(image)


def bsc_noise(tmr_arr):
    tmr_arr ^= np.random.random((len(tmr_arr),)) < p
    return tmr_arr


def gilbert_noise(tmr_arr):
    p_bg = 0.00000002
    p_gb = 0.0000002
    current_state = 'G'
    y = []
    for it9 in range(0, len(tmr_arr)):
        if current_state == 'G':
            if np.random.random() < p_gb:  # symulacja zmiany stanu z prawdopodobienstwiem pDZ
                current_state = 'B'  # zmiana stanu
            y.append(tmr_arr[it9])
        elif current_state == 'B':
            if np.random.random() < p_bg:
                current_state = 'G'
            y.append(1 - tmr_arr[it9])
    return y


print(x.shape)

np.random.seed(0)
x_TMR = []

for it in range(len(x)):
    for it2 in range(len(x[it])):
        for it3 in range(len(x[it][it2])):
            if x[it][it2][it3] == 1:
                x_TMR.extend([1]*3)
            elif x[it][it2][it3] == 0:
                x_TMR.extend([0]*3)


#z = bsc_noise(x_TMR)
z = gilbert_noise(x_TMR)
result = []
i = 0

while i < len(x_TMR):
    if z[i] & z[i+1] | z[i+1] & z[i+2] | z[i] & z[i+2]:
        result.append(1)
    else:
        result.append(0)
    i += 3

result = np.asarray(result)
result = result.reshape(223, 400, -1)

image_final = ldpc_images.Bin2RGB(result)
cv2.imwrite("outFileTMRGilbert_3.png", image_final)