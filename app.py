# Python standard libraries
import json

# Third-party libraries
from flask import Flask, redirect, request, render_template

# Airthings library
from AirthingsAccount import AirthingsAccount

# Get client id and secret from config.json
try:
    with open('config.json', 'r') as f:
        config_variables = json.load(f)
        AIRTHINGS_CLIENT_ID = config_variables['clientId']
        AIRTHINGS_CLIENT_SECRET = config_variables['clientSecret']
        APP_REDIRECT_URI = config_variables['redirectUri']
except FileNotFoundError:
    print('No config.json found')

# Basic flask app setup
app = Flask(__name__, static_url_path='/static', template_folder='templates')

# Initialize oauth2 for Airthings API
my_account = AirthingsAccount(
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
    redirect_url = my_account.get_authorization()
    return redirect(redirect_url, code=302)


@app.route("/callback")
def callback():
    my_account.get_access_token(request.url)
    return redirect("home", code=303)


@app.route("/devices")
def devices():
    data = my_account.get_devices(request.query_string)
    print(data)
    return render_template('index.html', data=json.dumps(data, sort_keys=True, indent=4))


@app.route("/devices/<device_id>")
def devices_with_id(device_id):
    data = my_account.get_devices(device_id, request.query_string)
    print(data)
    return render_template('index.html', data=json.dumps(data, sort_keys=True, indent=4))


@app.route("/locations")
def locations():
    data = my_account.get_locations(request.query_string)
    print(data)
    return render_template('index.html', data=json.dumps(data, sort_keys=True, indent=4))


@app.route("/devices/<device_id>/samples")
def samples(device_id):
    data = my_account.get_device_sample(device_id, request.query_string)
    print(data)
    return render_template('index.html', data=json.dumps(data, sort_keys=True, indent=4))


@app.route("/segments")
def segments():
    data = my_account.get_segments()
    print(data)
    return render_template('index.html', data=json.dumps(data, sort_keys=True, indent=4))


@app.route("/devices/<device_id>/latest-sample")
def latest_sample(device_id):
    data = my_account.get_latest_sample(device_id, request.query_string)
    print(data)
    return render_template('index.html', data=json.dumps(data, sort_keys=True, indent=4))


@app.route("/devices/<device_id>/threshold-breaches")
def threshold_breaches(device_id):
    data = my_account.get_threshold_breaches(device_id, request.query_string)
    print(data)
    return render_template('index.html', data=json.dumps(data, sort_keys=True, indent=4))


if __name__ == '__main__':
    app.run(debug=True, port=3000)
