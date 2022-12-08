import time
from time import sleep

import RPi.GPIO as GPIO
import serial

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)

GPIO.setup(12, GPIO.OUT, initial=GPIO.HIGH)


ser = serial.Serial(

    port='/dev/ttyAMA0',

    baudrate = 9600,

    parity=serial.PARITY_NONE,

    stopbits=serial.STOPBITS_ONE,

    bytesize=serial.EIGHTBITS,

    timeout=1

)


comunicaSolo = bytearray.fromhex('1C 03 01 21 05')
comunicaAr = bytearray.fromhex('1C 02 01 21 05')

ser.write(comunicaSolo)

print(comunicaSolo)

time.sleep(.02)
GPIO.setup(12, GPIO.OUT, initial=GPIO.LOW)


data_raw = ser.read(1)
if data_raw == b"\x1c":
    data_raw += ser.read_until(b'\x05')
    print(str(data_raw))
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    time.sleep(.02)