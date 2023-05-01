#!flask/bin/python
from flask import Flask
from Parking.parking_controller import parking_controller


app = Flask(__name__)
app.register_blueprint(parking_controller)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


