import RPi.GPIO as gp
import numpy as np

pins = [10, 9, 11, 5, 6, 13, 19, 26]
gp.setmode(gp.BCM)
gp.setup(pins, gp.OUT)
gp.setup(17, gp.OUT)


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


try:
    gp.output(17, True)
    while True:
        try:
            num = int(input('Enter value (-1 to exit) > '))
            if num == -1:
                exit(0)
            elif num < 0 or num > 255:
                print("Value out of range")
            else:
                num_dac(num)
                print("{} = {:.2f} V".format(num, 3.3 * num / 255))
        except ValueError:
            print("Try again...")
finally:
    num_dac(0)
    gp.cleanup()
`