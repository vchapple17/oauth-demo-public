from const import baseURL
import random
import string
import urllib
import hashlib
from google.appengine.ext import ndb
import uuid     # For unique random number for salt
import time

class Config:
    def __init__(self):
        self.client_id = "CLIENT_ID_HERE....apps.googleusercontent.com"
        self.client_secret = "CLIENT_SECRET_HERE..."
        self.redirect_uri = baseURL + "/oauth/callback"
        self.redirect_uri2 = baseURL + "/oauth/token"
        self.scope = "email"
        self.access_type = "online"
        self.include_granted_scopes = "true"
        self.prompt = "select_account"
        self.GoogleOAuthURL = "https://accounts.google.com/o/oauth2/auth"

        self.GoogleTokenURL = "https://accounts.google.com/o/oauth2/token"
        self.GoogleUserURL = "https://www.googleapis.com/oauth2/v2/userinfo"

        self.grant_type = "authorization_code"
        self.session_key = "SECRET_SESSION_KEY";

    def createState(self):
        # https://www.pythoncentral.io/hashing-strings-with-python/
        self.salt = uuid.uuid4().hex
        hash_obj = hashlib.sha256( self.salt.encode())
        hex_dig = hash_obj.hexdigest()
        self.state = hex_dig;

    def getURL(self):
        url = self.GoogleOAuthURL
        url += "?scope=" + str(self.scope)
        url += "&"
        url += "access_type=" + str(self.access_type)
        url += "&"
        url += "include_granted_scopes=" + str(self.include_granted_scopes)
        url += "&"
        url += "state=" + str(self.state)
        url += "&"
        url += "redirect_uri=" + str(self.redirect_uri)
        url += "&"
        url += "response_type=code"
        url += "&"
        url += "client_id=" + str(self.client_id)
        url += "&"
        url += "prompt=" + str(self.prompt)
        return url

    def getTokenURL(self):
        return str(self.GoogleTokenURL)

    def getTokenPayload(self, code):
        data = {}
        data['code'] = str(code)
        data['client_id'] = str(self.client_id)
        data['client_secret'] = str(self.client_secret)
        data['redirect_uri'] = str(self.redirect_uri)
        data['grant_type'] = str(self.grant_type)
        return data

    def getUserURL(self):
        return self.GoogleUserURL
