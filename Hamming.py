import numpy as np
import cv2
from pyldpc import ldpc_images

# Hamming codes with additional parity (SECDED)
# Macierze kodu Hamminga(8,4)

G = np.array([
    [1, 1, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 0, 0, 1],
    [0, 1, 0, 1, 0, 1, 0, 1],
    [1, 1, 0, 1, 0, 0, 1, 0]
])

H = np.array([
    [1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 1, 0, 0, 1, 1, 0],
    [0, 0, 0, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1]
])

R = np.array([
    [0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0]
])

def compareArr(before, after):
    counter = 0
    for els in range(0, len(before)):
        if before[els] != after[els]:
            counter += 1
    return counter


def bsc_noise(tmr_arr):
    p = 0.000001
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


def syndrome_fix(syndrome_vector_noised):
    index_to_fix = -1
    if np.array_equal(syndrome_vector_noised, np.zeros((4,), dtype=int)):
        return -1
    for columnIt in range(0, len(H)):
        if np.array_equal(syndrome_vector_noised, H.T[columnIt]):
            index_to_fix = columnIt
    return index_to_fix

image = cv2.imread("outFile_ITL_Gilbert_2.png", 1)
x = ldpc_images.RGB2Bin(image)
y = np.zeros_like(x)

input_data = np.zeros((4,), dtype=int)
it3 = 0
main_error_counter = 0
for it in range(len(x)):
    for it2 in range(len(x[it])):
        it3 = 0
        while it3 < len(x[it][it2]):

            input_data = np.copy(x[it][it2][it3:it3+4])

            data_vector = np.dot(input_data, G) % 2  # obliczony wektor danych
            noised_data = np.asarray(gilbert_noise(np.copy(data_vector)))   # Zaklocenie danych
            # noised_data = bsc_noise(np.copy(data_vector))
            error_counter = compareArr(data_vector, noised_data)
            syndrome_noised = np.dot(H, noised_data.T) % 2          # Syndrom oraz wykrycie bledu
            index_fix = syndrome_fix(syndrome_noised)
            if index_fix >= 0:
                noised_data[index_fix] = 1 - noised_data[index_fix]

            output_data = np.dot(R, noised_data.T)
            y[it][it2][it3:it3+4] = np.copy(output_data)
            it3 += 4
            main_error_counter += error_counter

image_final = ldpc_images.Bin2RGB(y)
cv2.imwrite("outFileHammingGilbert5.png", image_final)
print(main_error_counter)