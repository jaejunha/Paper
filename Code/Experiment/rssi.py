import os
import json
import time
import numpy as np
import math
from scipy import special
'''
Custom
'''
address = 'B0:C7:45:7D:06:60'
window = 100
thresh = -55
'''
Init
'''
list_data = []
list_result = []
total = 0
seq = -1
over = 0
est = 0.0
try:
        while True:
                str_result = os.popen('iwlist wlan0 scanning').readlines()
                collect = False
                for str_line in str_result:
                        if str_line.find('Address') >= 0:
                                if str_line.strip().split(' ')[4] == address:
                                        collect = True

                        if collect and str_line.find('Signal level') >= 0:
                                total += 1
                                seq = (seq + 1) % window
                                data = int(str_line.strip().split(' ')[3].split('=')[1])
				if math.isnan(est) or math.isinf(est):
                                        est = mean
                                print('real ' + str(data) +' / estimated ' + str(est))
                                list_result.append((data, est))
                                if total > window:
                                        if list_data[seq] < thresh:
                                                over -= 1
                                        if(data > thresh):
                                                over += 1
                                        list_data[seq] = data
                                else:
                                        if data > thresh:
                                                over += 1
                                        list_data.append(data)
                                break
                if total > window:
                        p = float(over) / window
                else:
                        p = float(over) / total
                mean = np.mean(list_data)
                std = np.std(list_data)
                est = math.sqrt(2)*special.erfinv(2 * p - 1)*std + mean
                print(total, p, mean)
                time.sleep(1)
except:
        for i in list_result:
                print(i)
