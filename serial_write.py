import time
from time import sleep

# import RPi.GPIO as GPIO
import serial

# GPIO.setwarnings(False)

# GPIO.setmode(GPIO.BOARD)

# GPIO.setup(7, GPIO.OUT, initial=GPIO.HIGH)


send = serial.Serial(

    port='/dev/ttyAMA0',

    baudrate = 9600,

    parity=serial.PARITY_NONE,

    stopbits=serial.STOPBITS_ONE,

    bytesize=serial.EIGHTBITS,

    timeout=1

)


i = [0,10,45,90,135,180,135,90,45,10,0]

while True:

 for x in i:

     send.write(x)

     print(x)

     time.sleep(1.5)