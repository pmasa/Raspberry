from pushbullet import Pushbullet
import RPi.GPIO as GPIO
from time import sleep
import requests
import json

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
pin_input = 3
GPIO.setup(pin_input, GPIO.IN)
pin_relay = 22
GPIO.setup(pin_relay, GPIO.OUT)
GPIO.output(pin_relay, False)

pb = Pushbullet("xxxxx")
print(pb.devices)
status = False

def getContacts(self):
        """ Gets your contacts
            https://docs.pushbullet.com/v2/contacts
            returns a list of contacts
        """
        return self._request("GET", HOST + "/contacts")["contacts"]

def _request(self, method, url, postdata=None, params=None, files=None):
        headers = {"Accept": "application/json",
                   "Content-Type": "application/json",
                   "User-Agent": "pyPushBullet"}

        if postdata:
            postdata = json.dumps(postdata)

        r = requests.request(method,
                             url,
                             data=postdata,
                             params=params,
                             headers=headers,
                             files=files,
                             auth=HTTPBasicAuth(self.apiKey, ""))

        r.raise_for_status()
        return r.json()


def pushNote(self, recipient, title, body, recipient_type="device_iden"):
        """ Push a note
            https://docs.pushbullet.com/v2/pushes
            Arguments:
            recipient -- a recipient
            title -- a title for the note
            body -- the body of the note
            recipient_type -- a type of recipient (device, email, channel or client)
        """

        data = {"type": "note",
                "title": title,
                "body": body}

        data[recipient_type] = recipient

        return self._request("POST", HOST + "/pushes", data)

def send_notification_via_pushbullet(title, body):
    """ Sending notification via pushbullet.
        Args:
            title (str) : title of text.
            body (str) : Body of text.
    """
    data_send = {"type": "note", "title": title, "body": body}
 
    ACCESS_TOKEN = 'xxxxx'
    resp = requests.post('https://api.pushbullet.com/v2/pushes', data=json.dumps(data_send),
                         headers={'Authorization': 'Bearer ' + ACCESS_TOKEN, 'Content-Type': 'application/json'})
    if resp.status_code != 200:
        raise Exception('Something wrong')
    else:
        print 'complete sending'

while True:
    i = GPIO.input(pin_input)
    if i == 1:
        GPIO.setup(pin_input, GPIO.IN)
        print ("Niveau OK")
        sleep(2)
        GPIO.output(pin_relay, False)
    elif i == 0:
        print ("Niveau d'eau atteint")
        gsm1 = pb.get_device('iPhone de TTTTT')
        push = gsm1.push_note("Alert !!", "Niveau d'innondation atteint")
	#push = pb.push_sms(gsm1, "+32476123456", "Alert innondation !!!")
        gsm2 = pb.devices[0]
	#myriam = pb.contact[0]
	#push = myriam.push_note("Alert !!", "Niveau d'innondation atteint")	
	print(gsm2)
	push = pb.push_sms(gsm2, "+32477123456", "Alert innondation !!!")
        #push = gsm2.push_note("Alert GSM2!!", "Niveau d'innondation atteint")
        #push = pb.push_note("Hello world!", "We're using the api.", contact="zzzzz")
	send_notification_via_pushbullet("Alert innondation!!", "Niveau d'innodation atteint")
	#contacts = pb.getContacts()
	#print(contacts)
	#pushNote(self, "yyyyy@gmail.com", "Alert!!!", "Niveau atteint", recipient_type="device_iden")
	sleep(2)
        GPIO.output(pin_relay, True)
