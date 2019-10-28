# Python standard libraries
import json
import os
# Third-party libraries
from flask import Flask, redirect, request, jsonify, render_template

# Airthings library
from AirthingsAccount import AirthingsAccount

AIRTHINGS_CLIENT_ID = ""
AIRTHINGS_CLIENT_SECRET = ""
APP_REDIRECT_URI = ""
# Get client id and secret from config.json
with open('config.json', 'r') as f:
    config_variables = json.load(f)
    AIRTHINGS_CLIENT_ID = config_variables['clientId']
    AIRTHINGS_CLIENT_SECRET = config_variables['clientSecret']
    APP_REDIRECT_URI = config_variables['redirectUri']
# Basic flask app setup
app = Flask(__name__, static_url_path='/static', template_folder='templates')

# Initialize oauth2 for Airthings API

myAccount = AirthingsAccount(
    client_id=AIRTHINGS_CLIENT_ID,
    client_secret=AIRTHINGS_CLIENT_SECRET,
    redirect_uri=APP_REDIRECT_URI
)

@app.route("/")
def index():
    return app.send_static_file('login.html')

@app.route("/home")
def home():
    return render_template('index.html')

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
    return render_template('index.html', data=json.dumps(data, sort_keys=True, indent=4))

@app.route("/devices/<deviceId>")
def devicesWithId(deviceId):
    data = myAccount.getDevices(deviceId)
    print(data)
    return render_template('index.html', data=json.dumps(data, sort_keys=True, indent=4))


@app.route("/locations")
def locations():
    data = myAccount.getLocations()
    print(data)
    return render_template('index.html', data=json.dumps(data, sort_keys=True, indent=4))


@app.route("/devices/<deviceId>/samples")
def samples(deviceId):
    data = myAccount.getDeviceSample(deviceId)
    print(data)
    return render_template('index.html', data=json.dumps(data, sort_keys=True, indent=4))

@app.route("/segments")
def segments():
    data = myAccount.getSegments()
    print(data)
    return render_template('index.html', data=json.dumps(data, sort_keys=True, indent=4))

@app.route("/devices/<deviceId>/latest-sample")
def latestSample(deviceId):
    data = myAccount.getLatestSample(deviceId)
    print(data)
    return render_template('index.html', data=json.dumps(data, sort_keys=True, indent=4))

@app.route("/devices/<deviceId>/threshold-breaches")
def thresholdBreaches(deviceId):
    data = myAccount.getThresholdBreaches(deviceId)
    print(data)
    return render_template('index.html', data=json.dumps(data, sort_keys=True, indent=4))

if __name__ == '__main__':
    app.run(debug=True, port=3000)
