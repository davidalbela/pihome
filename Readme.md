# Readme

Monitoring Apartment with Raspberry Pi, Prometheus & Grafana. 
A Pi Home python workshop based in original [pdambrauskas's Pi Home](https://github.com/pdambrauskas/pihome).

## Hardware components

- [Raspberry Pi 3 Model B](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/)
- 16 GB microSD card
- [DHT11 Temperature And Humidity Sensor](https://components101.com/dht11-temperature-sensor)
- [Motion Sensor HC-SR501](https://components101.com/hc-sr501-pir-sensor)
- Raspberry Pi Camera module.

## Python samples

https://gist.github.com/davidalbela/2367febf0d9e7811af54de6ece6040bc

## Install

1. Install Adafruit libraries
```
sudo pip3 install Adafruit_DHT
```

2. Install Docker & Docker-compose
```
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Give docker rights to Pi user
sudo usermod -aG docker pi
```

**NOTE**: Run exit and log in again to make sure `usermod` works.

3. Install Docker-compose
```
sudo apt install libffi-dev libssl-dev
sudo pip3 install docker-compose
sudo systemctl enable docker
```

## Create a web service

Go to flask path and follow steps:
1. Create sensor flask_app.py
```
#!/bin/env python

import Adafruit_DHT
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

sensor = Adafruit_DHT.DHT11

# TODO 
sensor_pin = # Indicar el pin GPIO donde se conecta el sensor

# Add webserver
from flask import Flask
app = Flask(__name__)

# TODO What is `/metrics`
@app.route('/metrics')
def metrics():
    umid, temp = Adafruit_DHT.read_retry(sensor, sensor_pin)
    if umid is not None and temp is not None:
        return '# HELP local_temp local temperature\n# TYPE local_temp gauge\nlocal_temp {}\n# HELP local_humidity local humidity\n# TYPE local_humidity gauge\nlocal_humidity {}\n'.format(int(temp), int(umid)), 200, {'Content-Type': 'text/plain; charset=utf-8'}
    else:
        return 'Could not read from DHT11.', 200, {'Content-Type': 'text/plain; charset=utf-8'}
```

2. Test flask
```
# Run the server
export FLASK_APP=/home/pi/flask_app.py
export FLASK_DEBUG=1
flask run --host=0.0.0.0 --port=5000

# Open other terminal and run
curl [pihome IP]:5000/metrics
```

Why `/metrics`?

Press Control + c to exit.

3. Create a run script `flash.sh` file
```
# Run nano flash.sh
#!/bin/bash

# flask settings
export FLASK_APP=/home/pi/flask_app.py
export FLASK_DEBUG=0

flask run --host=0.0.0.0 --port=5000

# Save and Run chmod +x flask.sh
```

4. Install `flash.sh` as a daemon
```
# Run cd /etc/systemd/system/
# Run sudo nano flask.service
[Unit]
Description = flask python command to do useful stuff

[Service]
ExecStart = /home/pi/flask.sh

[Install]
WantedBy = multi-user.target

# Save file
```

5. Run and enable flask as a daemon
```
sudo systemctl start flask
sudo systemctl enable flask.service
```

**NOTE**: Check service logs with journal:
```
journalctl -u flask.service
```

## Execute Monitoring System

1. Clone this repo
```
git clone https://github.com/davidalbela/pihome.git
cd pihome
```

2. Setup environment variables in `.env` file
```
nano .env
HOST_IP= # TODO paste here your Raspberry Pi IP
GRAFANA_PASSWORD= # TODO paste here a secure password for Grafana service
```

3. Execute Prometheus and Grafana as docker containers
```
docker-compose up -d
```

4. Check your containers
```
# list containers
docker ps

# read logs
docker logs grafana
docker logs -f prometheus
```

5. Visit your Raspberry Pi IP in your Laptop browser:
```
http:[Raspberry Pi IP]
```
Enter the user "admin" and your password configured in `.env` file (value for GRAFANA_PASSWORD).
