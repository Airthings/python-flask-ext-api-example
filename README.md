# Using the Airthings Api with Python and Flask

This sample code involves using a simple Flask webapp as a front-end interface using the request-oauthlib Python3 library to access the Airthings API using the Authorization Grant Oauth2 flow.

Please note that this is a basic example created only to show how to access information from the Airthings API. **Do not** use this code in production without first implementing standard security within your web application.

## Required Dependencies

* [Python 3](https://www.python.org/downloads/)
* [pip](https://packaging.python.org/tutorials/installing-packages/) to install the python packages for the project

## How to Use

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