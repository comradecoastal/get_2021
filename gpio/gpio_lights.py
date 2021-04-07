import RPi.GPIO as GPIO
import time

pinout = [24, 25, 8, 7, 12, 16, 20, 21]

GPIO.setmode(GPIO.BCM)

GPIO.setup(pinout, GPIO.OUT)

def lightUp(led, period):
    pin = pinout[led]
    GPIO.output(pin, 1)
    time.sleep(period)
    GPIO.output(pin, 0)

def blink(led, count, period):
    pin = pinout[led]
    for _ in range(count):
        GPIO.output(pin, 1)
        time.sleep(period)
        GPIO.output(pin, 0)
        time.sleep(period)

def runningLight(count, period):
    for _ in range(count):
        for i in range(8):
            GPIO.output(pinout[i], 1)
            time.sleep(period)
            GPIO.output(pinout[i], 0)

def runningDark(count, period):
    GPIO.output(pinout, 1)
    for _ in range(count):
        for i in range(8):
            GPIO.output(pinout[i], 0)
            time.sleep(period)
            GPIO.output(pinout[i], 1)
    GPIO.output(pinout, 0)

def decToBinList(val):
    out = [0]*8
    for i in range(7, -1, -1):
        if val // 2 ** i != 0:
            out[i] = 1
            val %= 2 ** i
    return out

def lightNumber(val):
    array = decToBinList(val)
    GPIO.output(pinout, array)

def runningPattern(val, direction):
    if direction > 0:
        while True:
            lightNumber(val)
            time.sleep(0.3)
            val = (val << 1) % 256 + (val << 1)  // 256
    else:
        while True:
            lightNumber(val)
            time.sleep(0.3)
            val = (val >> 1) % 256 + (val % 2) * 128

def lightPwm(led, cycles, step=0.1):
    p = GPIO.PWM(pinout[led], 50)
    p.start(0)
    for _ in range(cycles):
        for dc in range(0, 101, 5):
            p.ChangeDutyCycle(dc)
            time.sleep(step)
        for dc in range(100, -1, -5):
            p.ChangeDutyCycle(dc)
            time.sleep(step)
    p.stop()

lightUp(2, 2)

GPIO.output(pinout, 0)
GPIO.cleanup()