# Using the Airthings Api with Python and Flask

This sample code involves using a simple Flask webapp providing a front-end interface using the [requests-oauthlib](https://github.com/requests/requests-oauthlib) Python3 library to access the Airthings API using the Authorization Grant OAuth2 flow.

Please note that this is a basic example created only to show how to access information from the Airthings API. **Do not** use this code in production without first implementing standard security within your web application.

## Required Dependencies

* [Python 3](https://www.python.org/downloads/)
* [pip](https://packaging.python.org/tutorials/installing-packages/) to install the python packages for the project

## Installation

To setup the example Flask webapp simply run the following from the command line:
```
git clone https://github.com/Airthings/python-flask-ext-api-example
cd python-flask-ext-api-example
pip install -r requirements.txt
```

The webapp can then be run by using:
```
python app.py
```

<p align="center">
    <img src="https://i.imgur.com/V5aUwve.gif" width="65%"/>
</p>

## Basic Usage
Please refer to the [**Getting Started guide**](https://developer.airthings.com/docs/api.html) for a more generalized overview of accessing the the Airthings API.

Within this example the API can be accessed by supplying your:
* Airthings Client Id
* Airthings Client Secret
* Redirect URI