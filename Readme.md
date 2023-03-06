# Readme

https://gist.github.com/davidalbela/2367febf0d9e7811af54de6ece6040bc

See flask folder.

## Install 

Go to flask path and follow steps:
1. Create sensor flask_app.py

2. Test flask
```
export FLASK_APP=/home/pi/flask_app.py
flask run --host=0.0.0.0 --port=5000
curl [pihome IP]:5000/metrics
```

3. Create run script
```
#!/bin/bash
# flask settings
export FLASK_APP=/home/pi/flask_app.py
export FLASK_DEBUG=0

flask run --host=0.0.0.0 --port=5000

# Run chmod +x flask.sh
```

4. Install as a daemon
```
# Run cd /etc/systemd/system/
# Run sudo vim flask.service

[Unit]
Description = flask python command to do useful stuff

[Service]
ExecStart = /home/pi/flask.sh

[Install]
WantedBy = multi-user.target
```

5. Enable flask daemon
```
sudo systemctl enable flask.service
sudo systemctl flask start
```

## Install Docker & Docker compose

```
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo apt-get install libffi-dev libssl-dev

# Give docker rights to user. NOT SECURE for production!
sudo usermod -aG docker pi
exit # log out and log in again

# try Docker
docker version
docker run hello-world

# Install Docker Compose
sudo pip3 install docker-compose
sudo systemctl enable docker
```

## Run Prometheus and Grafana

```
git clone https://github.com/davidalbela/pihome.git
cd pihome

# TODO Setup env variables
touch .env
vim .env
HOST_IP=
GRAFANA_PASSWORD=

docker-compose up -d

# check running containers
docker ps

# check logs
docker logs -f grafana
docker logs -f prometheus
```

Visit your Raspberry Pi home IP in your browers :)

# Monitoring Apartment with Raspberry Pi, Prometheus & Grafana

For quite some time, I had a spare Raspberry Pi lying around in my place. And one weekend I came up with idea to make my apartment "smarter". What I mean by saying "smarter" is tracking some metrics of my surroundings.

I have some experience in working with [Prometheus](https://prometheus.io/) and [Grafana](https://grafana.com/), so I decided to incorporate those tools into my solution. Yes, it does sound like overengineering simple task, you can probably get same results in much simpler way : ).

By deploying this project with all its components, you'll be able to track these metrics:
- Room temperature
- Humidity
- Movement
- Nearby bluetooth devices
- Connected network devices

## Hardware components

These are all the component, I used in my project:
- [Raspberry Pi 3 Model B](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/)
- 16 GB microSD card
- [DHT11 Temperature And Humidity Sensor](https://components101.com/dht11-temperature-sensor)
- [Motion Sensor HC-SR501](https://components101.com/hc-sr501-pir-sensor)
- Mobile phone charger, for powering Raspberry Pi

## Connecting DHT11 Sensor to Raspberry Pi

I connected Ground pin to the Ground of Raspberry PI, Data Pin to GPIO 14 pin, Vcc pin to 3.3V power supply pin.

## Connecting HC-SR501 Sensor to Raspberry Pi

I connected Ground pin to the Ground of Raspberry PI, Data Pin to GPIO 17 pin, Vcc pin to 5V power supply pin.

## Reading sensor data

For reading DHT11 sensor data and feeding it to Prometheus, I chose [DHT11_Python](https://github.com/szazo/DHT11_Python) library, which is quite unstable, and sometimes does not return valid results, so you might get some gaps in your graphs.
For HC-SR501, I wrote simple python code myself.
You can browse source code of this project, for more details:
    - `application/temperature.py` & `application/dht11.py` for temperature & humidity readings;
    - `application/motion.py` for motion sensor;
    - `application/webapp.py` for prometheus endpoint.


## Prometheus configuration

To scrape metrics from my Flask API, I've added configuration to `prometheus.yml`:

```yaml
global:
    scrape_interval: 30s
scrape_configs:
    - job_name: 'pihome'
      static_configs:
        - targets: [pihome:5000]
```

## Grafana Configuration

Then, in `/etc/grafana/provisioning`, I've added datasource configuration:
```yaml
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    url: http://prometheus:9090/
    access: proxy
    isDefault: true
```
It is also possible to add Grafana dashboards to provisioning folder as json files, so that you don't need to create new dashboard each time you re-deploy Grafana.

## Connecting everything together

To make everything portable and easy to install, I packed my Flask API to Docker image and configured all services in `docker-compose.yaml`.
To deploy whole stack you have to add `.env` file with some configuration properties:
```
HOST_IP=192.168.1.216
NETWORK_TO_SCAN=192.168.1.0/24
GRAFANA_PASSWORD=pihome
```

After adding `.env`, file run `docker-compose build` & `docker-compose up -d`.

## Result

![](dashboard.png)

## Usefull resources

- https://www.freva.com/2019/05/21/hc-sr501-pir-motion-sensor-on-raspberry-pi/
- https://github.com/szazo/DHT11_Python