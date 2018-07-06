import reedsolo as reed
import cv2
import numpy as np

def compare_arr(arr_1, arr_2):
    counter = 0
    for it in range(0, len(arr_1)):
        if arr_1[it] != arr_2[it]:
            counter += 1
    print(counter)

def bsc_noise(tmr_arr):
    p = 0.001
    tmr_arr ^= np.random.random((len(tmr_arr), )) < p
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


def string_array(array):
    string = ''
    for i in range(0, len(array)):
        string += str(array[i])
    return string


def decToBin(number):# zamiana decymalnej na binarna
    return format(number, '08b')


def strToIntArray(string):# zamiana stringa na liste intow
    array = []
    for i in range(0, len(string)):
        array.append(int(string[i]))
    return array


rs = reed.RSCodec(12)
img = cv2.imread('inFile.png')
img_arr = np.array(img)

img_data = []
for i in range(0, len(img_arr)):
    for j in range(0, len(img_arr[i])):
        for z in range(0, len(img_arr[i][j])):
            img_data.append(img_arr[i][j][z])

img_data_bits = []
syncDAta = []
recivedData = []


for i in range(0, len(img_data)):
    current_byte = decToBin(img_data[i])
    current_byte = strToIntArray(current_byte)
    for j in range(0, len(current_byte)):
        img_data_bits.append(current_byte[j])

print("ilosc bitow:", len(img_data_bits))
key = (rs.encode(img_data_bits))
print("ilosc po zakodowaniu: ", len(key))

#przesłanie sygnału przez BSC
#transmission = bsc_noise(key)

#compare_arr(transmission, key)

#przesłanie sygnału przez Gilberta
transmission = gilbert_noise(key)

#dekodowanie i error correction
result = rs.decode(transmission)

print("po zdekodowaniu:")
compare_arr(result, img_data_bits)

byte_holder = []
bit_ctr = 0
byte_ctr = 0
output = []

for i in range(0, len(result)):
    byte_holder.append(result[i])
    bit_ctr += 1
    if bit_ctr == 8:
        byte_holder = string_array(byte_holder)
        img_data[byte_ctr] = int(byte_holder, 2)
        bit_ctr = 0
        byte_ctr += 1
        byte_holder = []

byte_counter = 0

for i in range(0, len(img_arr)):
    for j in range(0, len(img_arr[i])):
        for z in range(0, len(img_arr[i][j])):
            img_arr[i][j][z] = img_data[byte_counter]
            byte_counter += 1

cv2.imwrite('outFile_Reed_Solomon_BSC.png', img_arr)









