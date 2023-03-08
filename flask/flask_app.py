#!/bin/env python

import Adafruit_DHT
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

sensor = Adafruit_DHT.DHT11

# TODO 
sensor_pin = # Indicar el pin GPIO donde se conecta el sensor DHT11

# TODO (Opcional)
# motion_pin = # Indicar el pin de la variable motions del sensor PIR
# GPIO.setup(motion_pin, GPIO.IN)


# Add webserver
from flask import Flask
app = Flask(__name__)

@app.route('/metrics')
def metrics():
    umid, temp = Adafruit_DHT.read_retry(sensor, sensor_pin)
    # TODO  (Opcional)
    # motion = GPIO.input(motion_pin)
    if umid is not None and temp is not None:
        # TODO (Opcional) add "pihome_movement {} \n" to the returned text with the integer variable motions
        return '# HELP local_temp local temperature\n# TYPE local_temp gauge\nlocal_temp {}\n# HELP local_humidity local humidity\n# TYPE local_humidity gauge\nlocal_humidity {}\n'.format(int(temp), int(umid)), 200, {'Content-Type': 'text/plain; charset=utf-8'}
    else:
        return 'Could not read from DHT11.', 200, {'Content-Type': 'text/plain; charset=utf-8'}