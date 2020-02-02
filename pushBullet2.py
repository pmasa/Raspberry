from pushbullet import Pushbullet
import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
pin_input = 3
GPIO.setup(pin_input, GPIO.IN)
pin_relay = 22
GPIO.setup(pin_relay, GPIO.OUT)
GPIO.output(pin_relay, False)

pb = Pushbullet("o.Tc4lPsyu1U1vyRTwACB58zgJ2xFynMpC")
print(pb.devices)
status = False

while True:
    i = GPIO.input(pin_input)
    if i == 0:
        GPIO.setup(pin_input, GPIO.IN)
        print ("no motion")
        sleep(2)
        GPIO.output(pin_relay, False)
    elif i == 1:
        print ("motion")
        gsm1 = pb.get_device('iPhone de Pedro Masamuna')
        push = gsm1.push_note("Alert GSM1 !!", "Il y'a quelqu'un chez toi")
        gsm2 = pb.get_device('iPhone')
        push = gsm2.push_note("Alert GSM2!!", "Quelqu'un est dans ta maison")
        sleep(2)
        GPIO.output(pin_relay, True)
