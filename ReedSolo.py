import reedsolo as reed
import cv2
import numpy as np


def bsc_noise(tmr_arr):
    p = 0.001
    tmr_arr ^= np.random.random((len(tmr_arr), )) < p    # negate bits with a set probability
    return tmr_arr


def gilbert_noise(tmr_arr):
    p_bg = 0.00002
    p_gb = 0.0002
    current_state = 'G'
    y = []
    for it9 in range(0, len(tmr_arr)):
        if current_state == 'G':
            if np.random.random() < p_gb:  # Simulate the state change with a set probability
                current_state = 'B'
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


def dec_to_bin(number):
    return format(number, '08b')


def str_to_int_array(string):
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
receivedData = []

# Preparing the byte array for transmission
for i in range(0, len(img_data)):
    current_byte = dec_to_bin(img_data[i])
    current_byte = str_to_int_array(current_byte)
    for j in range(0, len(current_byte)):
        img_data_bits.append(current_byte[j])


key = (rs.encode(img_data_bits))

transmission = gilbert_noise(key)
# transmission = bsc_noise(key)

result = rs.decode(transmission)

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









