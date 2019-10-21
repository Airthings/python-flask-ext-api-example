# Python standard libraries
import json
import os
# Third-party libraries
from flask import Flask, redirect, request, jsonify

# Airthings library
from AirthingsAccount import AirthingsAccount

# Get client id and secret from environment variables
AIRTHINGS_CLIENT_ID = os.environ.get("AIRTHINGS_CLIENT_ID", None)
AIRTHINGS_CLIENT_SECRET = os.environ.get("AIRTHINGS_CLIENT_SECRET", None)

# Basic flask app setup
app = Flask(__name__, static_url_path='/static') # set static pat

# Initialize oauth2 for Airthings API
myAccount = AirthingsAccount(
    client_id=AIRTHINGS_CLIENT_ID,
    client_secret=AIRTHINGS_CLIENT_SECRET,
    redirect_uri="https://localhost:3000/callback"
)

@app.route("/")
def index():
    return '<a href="/auth">Log in with Airthings</a>'

@app.route("/home")
def home():
    return app.send_static_file('home.html')

@app.route("/auth")
def auth():
    redirect_url = myAccount.getAuthorization()
    return redirect(redirect_url, code=302)

@app.route("/callback")
def callback():
    myAccount.getAccessToken(request.url)
    return redirect("home", code=303)

@app.route("/devices")
def devices():
    data = myAccount.getDevices()
    print(data)
    return jsonify(data)

@app.route("/devices/<deviceId>")
def devicesWithId(deviceId):
    data = myAccount.getDevices(deviceId)
    print(data)
    return jsonify(data)

@app.route("/locations")
def locations():
    data = myAccount.getLocations()
    print(data)
    return jsonify(data)

@app.route("/devices/<deviceId>/samples")
def samples(deviceId):
    data = myAccount.getDeviceSample(deviceId)
    print(data)
    return jsonify(data)

@app.route("/segments")
def segments():
    data = myAccount.getSegments()
    print(data)
    return jsonify(data)

@app.route("/devices/<deviceId>/latest-sample")
def latestSample(deviceId):
    data = myAccount.getLatestSample(deviceId)
    print(data)
    return jsonify(data)

@app.route("/devices/<deviceId>/threshold-breaches")
def thresholdBreaches(deviceId):
    data = myAccount.getThresholdBreaches(deviceId)
    print(data)
    return jsonify(data)

if __name__ == '__main__':
    app.run(ssl_context='adhoc', debug=True, port=3000)
