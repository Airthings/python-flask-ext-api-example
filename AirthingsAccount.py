# coding=utf-8
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import TokenExpiredError
import os
import json
import logging
import logging.config

# Allows oauth to run in debug mode
# Remove this from production code
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


class AirthingsAccount:
    authorization_url = "https://accounts.airthings.com/authorize"
    token_url = "https://accounts-api.airthings.com/v1/token"
    ext_url = "https://ext-api.airthings.com/v1/"
    client = None
    access_token = ""
    refresh_token = ""
    expires_in = ""

    def __init__(self, client_id, client_secret, redirect_uri):
        self.logger = logging.getLogger(__name__)
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.oauth = OAuth2Session(client_id=self.client_id, redirect_uri=self.redirect_uri, scope=['read:device'])

    def get_endpoint(self, endpoint, query_string=None):
        query_string = query_string.decode('utf-8')
        try:
            r = self.client.get(f"{self.ext_url}{endpoint}{f'?{query_string}' if query_string else ''}")
            return json.loads(r.content)
        except TokenExpiredError:
            self.client.refresh_token(self.token_url)
            r = self.client.get(f"{self.ext_url}{endpoint}{f'?{query_string}' if query_string else ''}")
            return json.loads(r.content)

    def get_devices(self, device_id=None, query_string=None):
        if device_id:
            return self.get_endpoint(f"devices/{device_id}", query_string)
        else:
            return self.get_endpoint("devices", query_string)

    def get_latest_sample(self, device_id, query_string=None):
        return self.get_endpoint(f"devices/{device_id}/latest-samples", query_string)

    def get_threshold_breaches(self, device_id, query_string=None):
        return self.get_endpoint(f"devices/{device_id}/threshold-breaches", query_string)

    def get_latest_segment(self, device_id, query_string=None):
        return self.get_endpoint(f"devices/{device_id}/latest-segment", query_string)

    def get_device_sample(self, device_id, query_string=None):
        return self.get_endpoint(f"devices/{device_id}/samples", query_string)

    def get_locations(self, query_string=None):
        return self.get_endpoint("locations", query_string)

    def get_segments(self, query_string=None):
        return self.get_endpoint("segments", query_string)

    def get_samples_from_segment(self, segment, query_string=None):
        return self.get_endpoint(f"segments/{segment}/samples", query_string)

    def get_access_token(self, auth_url):
        if not self.client:
            authorization_response = auth_url
            token = self.oauth.fetch_token(
                token_url=self.token_url,
                client_id=self.client_id,
                include_client_id=True,
                client_secret=self.client_secret,
                authorization_response=authorization_response
            )
            if token:
                self.client = self.oauth
                self.access_token = token['access_token']
                self.refresh_token = token['refresh_token']
                self.expires_in = token['expires_in']
            else:
                return json.loads('{"Error":"Token credentials incorrect. Check your secret or client id"}')
        else:
            self.logger.error('Error occurred, you have already fetched your access token.')
            return json.loads('{"Error":"Access token already fetched."}')

    def get_authorization(self):
        self.logger.info('Getting authorization from Accounts')
        try:
            authorization_url, state = self.oauth.authorization_url(self.authorization_url)
            return authorization_url
        except:
            self.logger.error('Error occurred, check if your client id, client secret or redirect URI are correct.')
            return {}
