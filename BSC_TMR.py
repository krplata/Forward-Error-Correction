import numpy as np
import cv2
from pyldpc import ldpc_images


image = cv2.imread("inFile.png", 1)
x = ldpc_images.RGB2Bin(image)
print(x.shape)
p = 0.05
np.random.seed(0)
x_TMR = []

for it in range(len(x)):
    for it2 in range(len(x[it])):
        for it3 in range(len(x[it][it2])):
            if x[it][it2][it3] == 1:
                x_TMR.extend([1]*3)
            elif x[it][it2][it3] == 0:
                x_TMR.extend([0]*3)

print(len(x_TMR))
x_TMR ^= np.random.random((len(x_TMR),)) < p

y = []
i = 0

while i < len(x_TMR):
    if x_TMR[i] & x_TMR[i+1] | x_TMR[i+1] & x_TMR[i+2] | x_TMR[i] & x_TMR[i+2]:
        y.append(1)
    else:
        y.append(0)
    i += 3

y = np.asarray(y)
y = y.reshape(223, 400, -1)

image_final = ldpc_images.Bin2RGB(y)
cv2.imwrite("outFileBSC.png", image_final)
