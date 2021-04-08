import numpy as np
import time
from matplotlib import pyplot as plt
import scipy.io.wavfile

import RPi.GPIO as gp

# pins = [24, 25, 8, 7, 12, 16, 20, 21]
pins = [10, 9, 11, 5, 6, 13, 19, 26]

SAMPLE = 10e-6

gp.setmode(gp.BCM)

gp.setup(pins, gp.OUT)


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


def triangle_wave(delay=0.001):
    for i in range(256):
        num_dac(i)
        time.sleep(delay)
    for i in range(255, -1, -1):
        num_dac(i)
        time.sleep(delay)


def sine_array(frq, time_val):
    sample = SAMPLE
    time_function = np.round((np.sin(2 * np.pi * frq * np.arange(0, time_val, sample)) + 1) * 255 / 2)
    plt.plot(np.arange(0, time_val, sample), time_function)
    plt.title('Синус')
    plt.xlabel('Время')
    plt.ylabel('Амплитуда sin(time)')
    plt.ylim([-10, 265])
    plt.xlim([0, time_val])
    plt.grid(True)
    plt.yticks([0, 64, 128, 196, 255])
    plt.show()
    return time_function


def array_play(array, sample_time):
    for val in array:
        num_dac(val)
        time.sleep(0)


try:
    if __name__ == '__main__':
        sr, array = scipy.io.wavfile.read('/home/gr004/Desktop/coastal/gpio/SOUND.WAV')

        # sr /= 2
        # array = array[::8]
        shape = np.shape(array)
        sample_time = float(1 / sr)
        print(sample_time)
        channels = array.shape[1]
        print(channels)
        length = array.shape[0] / sr 
        print(array.shape[0] / sr)

        maxim_yun = np.max(array[:, 0])
        print(maxim_yun)

        array = array / (1 << 8) + 128
        array = np.round(array)

        # time = np.linspace(0. , length, array.shape[0])
        # plt.plot(time, array[:, 0])
        # plt.show()

        
        array_play(array[:, 0], sample_time)
        # elif len(shape) == 2:
        #     array = array[:, 1]
        #     array_play(array, sample_time)
finally:
    num_dac(0)
    gp.cleanup()

