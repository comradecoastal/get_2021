import numpy as np
import time

# import RPi.GPIO as gp

pins = [24, 25, 8, 7, 12, 16, 20, 21]
#
# gp.setmode(gp.BCM)
#
# gp.setup(pins, gp.OUT)


def dec_to_bin_list(val):
    out = [0] * 8
    for i in range(7, -1, -1):
        if val // 2 ** i != 0:
            out[i] = 1
            val %= 2 ** i
    return out


def num_dac(val):
    array = dec_to_bin_list(val)
    # gp.output(pins, array)
    print(array)


def triangle_wave(delay=0.001):
    for i in range(256):
        num_dac(i)
        time.sleep(delay)
    for i in range(255, -1, -1):
        num_dac(i)
        time.sleep(delay)


if __name__ == '__main__':
    print('To exit enter "-1"')
    while True:
        try:
            value = int(input('Please the number of repetitions: '))
            if value > -1:
                for i in range(value):
                    triangle_wave()
            elif value == -1:
                num_dac(0)
                # gp.cleanup()
                exit()
            elif value > 255 or value < -1:
                print('The value entered is out of range.')
        except ValueError:
            print('The value entered is not an integer.')
        except KeyboardInterrupt:
            num_dac(0)
            # gp.cleanup()
            exit()

