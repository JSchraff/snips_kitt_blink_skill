#!/usr/bin/env python3

import paho.mqtt.client as mqtt



# if this skill is supposed to run on the satellite,
# please get this mqtt connection info from <config.ini>
#
# hint: MQTT server is always running on the master device
MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883


from threading import Thread
import time
import RPi.GPIO as GPIO
import os

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
sweep = [23, 18, 16, 20, 12, 24, 25, 21, 25, 24, 12, 20, 16, 18]

for pin in sweep:
    GPIO.setup(pin, GPIO.OUT)


def playSound(filename, siteId):
    fp = open('file.wav', 'rb')
    f = fp.read()
    client.publish('hermes/audioServer/{}/playBytes/'.format(siteId), bytearray(f))


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
    #playThread.start()
    blinkThread.start()

def stopListen():
    global blinking
    blinking = False

def on_message(client, userdata, msg):
    if msg.topic == "hermes/dialogueManager/sessionStarted":
        startListen()
    elif msg.topic == "hermes/dialogueManager/sessionEnded":
        stopListen()
    elif msg.topic == "hermes/hotword/default/detected":
        playSound("scannerSweep.wav", "default")
    #elif msg.topic == "hermes/asr/textCaptured":
    #elif msg.topic == "hermes/nlu/intentNotRecognized":



if __name__ == "__main__":
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(MQTT_IP_ADDR, MQTT_PORT, 60)
    client.subscribe("#")
    client.loop_forever()
