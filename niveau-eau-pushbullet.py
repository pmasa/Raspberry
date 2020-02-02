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
    if i == 1:
        GPIO.setup(pin_input, GPIO.IN)
        print ("Niveau OK")
        sleep(2)
        GPIO.output(pin_relay, False)
    elif i == 0:
        print ("Niveau d'eau atteint")
        gsm1 = pb.get_device('iPhone de Pedro Masamuna')
        push = gsm1.push_note("Alert !!", "Niveau d'innondation atteint")
        #gsm2 = pb.get_device('iPhone')
        #push = gsm2.push_note("Alert GSM2!!", "Niveau d'innondation atteint")
        sleep(2)
        GPIO.output(pin_relay, True)
