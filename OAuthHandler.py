#!/usr/bin/env python
from BaseHandler import BaseHandler
from config import Config
from const import baseURL

from webapp2 import redirect
import json
import os
from google.appengine.ext.webapp import template
import urllib
from google.appengine.api import urlfetch

class OAuthHandler(BaseHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, {"url": baseURL}))

class AuthorizeHandler(BaseHandler):
    def get(self):
        config = Config()
        config.createState()
        self.session['state'] = config.state    # Save state
        self.redirect(config.getURL())          # Redirect to Google

class CallbackHandler(BaseHandler):
    def get(self):

        # CHECK FOR ERROR
        err = self.request.get("error");
        if (err != ""):
            print("ERROR")
            path = os.path.join(os.path.dirname(__file__), '500.html')
            self.response.out.write(template.render(path, {"url": baseURL}))
            return

        # Check state is valid
        state = self.request.get("state");
        if (state != self.session.get('state')):
            self.response.write("Invalid State Request");
            self.session['state'] = ""
            return;

        # Get authorization code from parameters
        code = self.request.get("code");

        # Create URL to get token using getTokenURL( code )
        config = Config()
        url = config.getTokenURL()
        try:
            data = config.getTokenPayload( code );
            edata = urllib.urlencode(data)
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            res = urlfetch.fetch(
                url=url,
                payload=edata,
                method=urlfetch.POST,
                headers=headers
            )
        except:
            # Report error
            # self.response.out.write({"error": "Error redeaming token."})
            print("ERROR")
            path = os.path.join(os.path.dirname(__file__), '500.html')
            self.response.out.write(template.render(path, {"url": baseURL}))
            return

        # Save access_token to session
        payload = json.loads(res.content)
        self.session['access_token'] = payload['access_token']
        self.session['token_type'] = payload['token_type']

        # REDIRECT USER TO token handler
        self.redirect(config.redirect_uri2);

class OAuthTokenHandler(BaseHandler):
    def get(self):
        # Get parameter access_token
        token = self.session.get('access_token')

        # Get User's JSON from google plus
        config = Config()

        try:
            url = config.getUserURL()
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                "Authorization": "Bearer %s" % token
            }
            res = urlfetch.fetch(
                url=url,
                headers=headers
            )
        except:
            self.response.write(res.content)
            self.session['access_token'] = ""
            self.session['token_type'] = ""
            return

        # Valid results of response
        payload = json.loads(res.content)

        # Deal with authentication error
        if 'error' in payload:
            print("ERROR")
            path = os.path.join(os.path.dirname(__file__), '500.html')
            self.response.out.write(template.render(path, {"url": baseURL}))
            return

        # Grab data for handler page
        context = {}
        context['url'] = baseURL
        try:
            # Send Name to context
            if 'name' in payload and payload['name'] != "":
                context['name'] = payload['name']
            else:
                context['name'] = "No Name Provided"
                context['email'] = payload['email']

            # Send Link to context
            if 'link' in payload:
                context['link'] = payload['link']

            # Send State to context
            context['state'] = self.session.get('state')
        except:
            print("500 - error")
            path = os.path.join(os.path.dirname(__file__), '500.html')
            self.response.out.write(template.render(path, {"url": baseURL}))
            return
        print(context)
        # Send context to HTML
        path = os.path.join(os.path.dirname(__file__), 'success.html')
        self.response.out.write(template.render(path, context))
