from flask import Flask
from Parking.parking_controller import parking_controller


app = Flask(__name__)
app.register_blueprint(parking_controller)

# export FLASK_RUN_HOST=0.0.0.0
# export FLASK_APP=app.py
# export FLASK_RUN_PORT=8080

if __name__ == '__main__':
    app.run()


