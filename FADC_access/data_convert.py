# -*- coding: utf-8 -*-
import numpy as np



file_path = "/dybfs2/nEXO/fuys/test_20230927_112850.dat"
# file_path = "/dybfs2/nEXO/fuys/data/miniTPC_data/from_miao/test_20230921_160524.dat"


with open(file_path, 'rb') as file:


    data_blocks = []
    count = 0
    # while True:
    while count<2e7:
    # while True:
        try:
            hex_data = file.read(16)  
            if not hex_data:
                break

            decimal_data = [int(byte) * 256 + int(hex_data[i+1]) for i, byte in enumerate(hex_data) if i % 2 == 0]
            data_blocks.append(decimal_data)
            count+=1

        except Exception as e:
            print(f"Error processing data block:{e}")
            continue  



data_array = np.array(data_blocks)
np.save('./data/data_array_0927_10MHZ_comb.npy', data_array)

