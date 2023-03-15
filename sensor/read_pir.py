#!/bin/env python

import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# TODO
GPIO.setup(, GPIO.IN) # Indicar pin de lectura del PIR motion sensor

while True:
  # TODO
  i = GPIO.input() # Indicar pin de lectura del PIR motion sensor
  if i==0:
    print "No intruders", i    
  else:
    print "Intruder detected", i

  time.sleep(0.1)