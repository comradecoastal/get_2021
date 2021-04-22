import RPi.GPIO as gp
import numpy as np
import time

pins = [10, 9, 11, 5, 6, 13, 19, 26]
gp.setmode(gp.BCM)
gp.setup(pins, gp.OUT)
gp.setup(17, gp.OUT)
gp.setup(4, gp.IN)


def dec_to_bin_list(val):
    out = [0] * 8
    for i in range(7, -1, -1):
        if val // 2 ** i != 0:
            out[i] = 1
            val %= 2 ** i
    return out


def num_dac(val):
    array = dec_to_bin_list(val)
    gp.output(pins, array)
    # print(array)


num_dac(0)
gp.output(17, True)

try:
    while True:
        for i in range(255):      
            num_dac(i)
            time.sleep(0.001)
            if not gp.input(4):
                print('Voltage: {:.1f}, digital value: {}'.format(3.3 * i /255, i))
                break
        
    
finally:
    num_dac(0)
    gp.cleanup()
