#!/bin/bash

# flask settings
export FLASK_APP=/home/pi/flask_app.py
export FLASK_DEBUG=0

flask run --host=0.0.0.0 --port=5000

# TODO dar permisos de ejecución
# Run chmod +x flask.sh