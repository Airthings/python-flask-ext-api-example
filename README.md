# Accessing the Airthings Api with Python and Flask

This sample code involves using a simple Flask webapp providing a front-end interface using the [requests-oauthlib](https://github.com/requests/requests-oauthlib) Python3 library to access the Airthings for Business API using the Authorization Grant OAuth2 flow.

Please note that this is a basic example created only to show how to access information from the Airthings API. **Do not** use this code in production without first implementing standard security within your web application.

## Required Dependencies

* [Python 3](https://www.python.org/downloads/)
* [pip](https://packaging.python.org/tutorials/installing-packages/) to install the python packages for the project

### Compatibility
This example is built to work with the Airthings for Business API.

## Installation

To set up the example Flask webapp simply run the following from the command line:
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

Before starting ensure you have your credentials:
* Airthings Client Id
* Airthings Client Secret
* Redirect URI
All three can be found at https://accounts.airthings.com/clients when registering an API Client.

### Adding Configuration and Gaining Access Token

The `AirthingsAccount` class within the `AirthingsAccount.py` file can be used to begin the OAuth2 flow. The class can be initialised with by being supplied with the API credentials. **Three steps must be followed to gain an access token**:

#### Step 1

Initialize the AirthingsAccount with your API credentials.

```python
my_account = AirthingsAccount(
    client_id     = AIRTHINGS_CLIENT_ID,
    client_secret = IRTHINGS_CLIENT_SECRET,
    redirect_uri  = APP_REDIRECT_URI
)
```
#### Step 2

The `get_authorization` function returns an authorization URL that will provide a link provided by Airthings that will let you log into your account via username and password. Upon logging in you will then be redirected to the *redirect URI* that you provided.

```python
my_account.get_authorization()
```

#### Step 3

Ideally, the *redirect URI* will contain a `code` that can be used to fetch access tokens. The `get_access_token` function can be provided with the redirected page URL you were sent to from the previous step to allow you to get your access token.

```python
my_account.get_access_token(request.url)
```

#### Making Requests

Currently, only `GET` requests are supported, which are listed in the [API documentation](https://accounts.airthings.com/api-docs). The routes defined in the `app.py` file detail how these requests can be made, while the `index.html` can display basic JSON results.

### Securing API Credentials

There are a number of ways to supply API credentials to the `AirthingsAccount` class. It is critical to never include client secrets within your web app directly. This can lead to a number of security risks that may compromise your account information.

