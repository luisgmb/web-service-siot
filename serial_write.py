import time
from time import sleep

import RPi.GPIO as GPIO
import serial

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)

GPIO.setup(12, GPIO.OUT, initial=GPIO.HIGH)


send = serial.Serial(

    port='/dev/ttyAMA0',

    baudrate = 9600,

    parity=serial.PARITY_NONE,

    stopbits=serial.STOPBITS_ONE,

    bytesize=serial.EIGHTBITS,

    timeout=1

)


comunicaSolo = bytearray.fromhex('1C 03 01 21 05')
comunicaAr = bytearray.fromhex('1C 02 01 21 05')

while True:

 send.write(comunicaSolo)

 print(comunicaSolo)

 time.sleep(1.5)