import numpy as np
import cv2
from pyldpc import ldpc_images

image = cv2.imread("inFile.png", 1)
x = ldpc_images.RGB2Bin(image)

p = 0.000000001
np.random.seed(0)
x = x.flatten()
print(x.shape)
x ^= np.random.random(len(x)) < p
x = x.reshape(223, 400, 24)

image_final = ldpc_images.Bin2RGB(x)
cv2.imwrite("outFileBSC8.png", image_final)
