# coding=utf-8
import requests
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


    def getEndpoint(self, endpoint):
        try:
            r = self.client.get(self.ext_url + endpoint)
            return json.loads(r.content)
        except TokenExpiredError:
            self.client.refresh_token(self.token_url)
            r = self.client.get(self.ext_url + endpoint)
            return json.loads(r.content)

    def getDevices(self, deviceId=None):
        if deviceId:
            return self.getEndpoint('devices/' + deviceId)
        else:
            return self.getEndpoint('devices')
    
    def getLatestSample(self, deviceId):
        return self.getEndpoint('devices/' + deviceId + '/latest-samples')

    def getThresholdBreaches(self, deviceId):
        return self.getEndpoint('devices/' + deviceId + '/threshold-breaches')

    def getLatestSegment(self, deviceId):
        return self.getEndpoint('devices/' + deviceId + '/latest-segment')

    def getDeviceSample(self, deviceId):
        return self.getEndpoint('devices/' + deviceId + '/samples')

    def getLocations(self):
        return self.getEndpoint('locations')

    def getSegments(self):
        return self.getEndpoint('segments')
    
    def getSamplesFromSegment(self, segment):
        return self.getEndpoint('segments' + segment + '/samples')

    def getAccessToken(self, authurl):
        if not self.client:
            authorization_response = authurl
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

    def getAuthorization(self):
        self.logger.info('Getting authorization from Accounts')
        try:    
            authorization_url, state = self.oauth.authorization_url(self.authorization_url)
            return authorization_url
        except:
            self.logger.error('Error occurred, check if your client id, client secret or redirect URI are correct.')
            return {}
