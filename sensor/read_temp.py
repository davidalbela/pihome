#!/bin/env python

import Adafruit_DHT  
import time  
 
while True:
  sensor = Adafruit_DHT.DHT11
  
  # TODO
  pin =  # Indicar el pin GPIO donde se conecta el sensor
  
  humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
  print ('Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity))
  
  time.sleep(1)