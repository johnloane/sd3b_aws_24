import RPi.GPIO as GPIO
import time
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener
from dotenv import load_dotenv
import os
import json

load_dotenv()

sensors_list = ["buzzer"]
data = {}

class Listener(SubscribeListener):
    def status(self, pubnub, status):
        print(f'Status: \n{status.category.name}')
    
config = PNConfiguration()
config.subscribe_key = os.getenv("PUBNUB_SUBSCRIBE_KEY")
config.publish_key = os.getenv("PUBNUB_PUBLISH_KEY")
config.secret_key = os.getenv("PUBNUB_SECRET_KEY")
#config.cipher_key = os.getenv("PUBNUB_CIPHER_KEY")
config.user_id = "johns-pi-0"


pubnub = PubNub(config)
pubnub.add_listener(Listener())

app_channel = "sd3b-iot-channel"

subscription = pubnub.channel(app_channel).subscription()
subscription.on_message= lambda message: handle_message(message)
subscription.subscribe()

publish_result = pubnub.publish().channel(app_channel).message("Hello from John's pi").sync()

def handle_message(message):
    print(message.message)
    msg = json.loads(json.dumps(message.message))
    if 'message' in msg:
        buzzer = msg['message']['buzzer']
        if buzzer == 'on':
            data["alarm"] = True
        elif buzzer == 'off':
            data["alarm"] = False

PIR_pin = 23
Buzzer_pin = 24

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_pin, GPIO.IN)
GPIO.setup(Buzzer_pin, GPIO.OUT)

def main():
    motion_detection()

def motion_detection():
    data["alarm"] = False
    trigger = False
    while True:
        if GPIO.input(PIR_pin):
            print("Motion detected")
            beep(4)
            trigger = True
            pubnub.publish().channel(app_channel).message('"Motion":"Yes"').sync()
            time.sleep(1)
        elif trigger:
            pubnub.publish().channel(app_channel).message('"Motion":"No"').sync()
            trigger = False

        if data["alarm"]:
            beep(2)


def beep(repeat):
    for i in range(0, repeat):
        for pulse in range(60):
            GPIO.output(Buzzer_pin, True)
            time.sleep(0.001)
            GPIO.output(Buzzer_pin, False)
            time.sleep(0.001)
        time.sleep(0.02)

if __name__ == "__main__":
    main()
