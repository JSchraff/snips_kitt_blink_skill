#!/usr/bin/env python3

# if this skill is supposed to run on the satellite,
# please get this mqtt connection info from <config.ini>
#
# hint: MQTT server is always running on the master device
MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883


import paho.mqtt.client as mqtt
from threading import Thread
import time
import RPi.GPIO as GPIO
import json
import random

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
sweep = [23, 18, 16, 20, 12, 24, 25, 21, 25, 24, 12, 20, 16, 18]

for pin in sweep:
    GPIO.setup(pin, GPIO.OUT)



def blink():
    global blinking
    blinking = True
    pins = sweep[:]
    pin = pins[len(pins) - 1]
    while blinking:
        if len(pins) == 0:
            pins = sweep[:]
        oldpin = pin
        pin = pins.pop()
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(0.05)
        GPIO.output(oldpin, GPIO.LOW)
        time.sleep(0.1)
    GPIO.output(pin, GPIO.LOW)



blinkThread = Thread(target=blink)

def startListen():
    blinkThread = Thread(target=blink)
    blinkThread.start()

def stopListen():
    global blinking
    blinking = False
    blinkThread.join()

def on_message(client, userdata, msg):
    if msg.topic == "hermes/dialogueManager/sessionStarted":
        startListen()
        client.publish("hermes/tts/say",
                       '{"siteId":"default", "lang":"de_DE", "text": "[[sound:scannerSweep]]", "id": "23", "sessionId": "45"}')#.format(json.load(msg.payload)["siteId"]))

    elif msg.topic == "hermes/dialogueManager/sessionEnded":
        stopListen()
    elif msg.topic == "hermes/asr/textCaptured":
        pass
    elif msg.topic == "hermes/nlu/intentNotRecognized":
        pass


def registerSound():
    fp = open('scannerSweep.wav', 'rb')
    f = fp.read()
    client.publish("hermes/tts/registerSound/scannerSweep", bytearray(f))
    client.publish("hermes/feedback/sound/toggleOff", '{"siteId": "default"}') #turn standard sound off
    fp.close()


if __name__ == "__main__":
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(MQTT_IP_ADDR, MQTT_PORT, 60)
    client.subscribe("#")
    registerSound()
    client.loop_forever()
