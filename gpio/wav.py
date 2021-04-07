import numpy as np
import time
from matplotlib import pyplot as plt
import scipy.io.wavfile

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
    # print(array)


def triangle_wave(delay=0.001):
    for i in range(256):
        num_dac(i)
        time.sleep(delay)
    for i in range(255, -1, -1):
        num_dac(i)
        time.sleep(delay)


def sine_array(frq, time_val):
    sample = 10e-3
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
        time.sleep(sample_time)


if __name__ == '__main__':
    sr, array = scipy.io.wavfile.read('SOUND.WAV')
    shape = np.shape(array)
    sample_time = 1 / sr
    if len(shape) == 1:
        array_play(array, sample_time)
    elif len(shape) == 2:
        array = array[:, 1]
        array_play(array, sample_time)

