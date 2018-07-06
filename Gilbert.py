import numpy as np
import cv2
from pyldpc import ldpc_images


# stałe prawdopodobieństwa
pD = 1
pZ = 0
pZD = 0.002
pDZ = 0.02

image = cv2.imread("inFile.png", 1)
x = ldpc_images.RGB2Bin(image)
y = []

current_state = 'G'

for it in range(0, len(x)):
    for it2 in range(0, len(x[it])):
        for it3 in range(0, len(x[it][it2])):
            if current_state == 'G':
                if np.random.random() < pDZ:  # symulacja zmiany stanu z prawdopodobienstwiem pDZ
                    current_state = 'B'  # zmiana stanu
                if np.random.random() < pD:
                    y.append(x[it][it2][it3])
                else:
                    y.append(1 - x[it][it2][it3])
            elif current_state == 'B':
                if np.random.random() < pZD:
                    current_state = 'G'
                if np.random.random() < pZ:     # Sprawdź prawdopodobieństwa
                    y.append(1 - x[it][it2][it3])
                else:
                    y.append(x[it][it2][it3])

y = np.asarray(y)
y = y.reshape(223, 400, -1)

image_final = ldpc_images.Bin2RGB(y)
cv2.imwrite("outFileGilbert.png", image_final)
