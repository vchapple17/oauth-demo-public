#!/usr/bin/env python

import webapp2
from webapp2 import Route
from webapp2_extras import sessions
from OAuthHandler import OAuthHandler, OAuthAuthorizeHandler, OAuthCallbackHandler, OAuthTokenHandler
from config import Config


conf = Config()
configuration = {}
configuration['webapp2_extras.sessions'] = {
    'secret_key': conf.session_key,
}

# Routes
application = webapp2.WSGIApplication([
    Route('/', handler=OAuthHandler, name='oauth'),
    Route('/oauth', handler=OAuthHandler, name='oauth'),
    Route('/oauth/', handler=OAuthHandler, name='oauth'),
    Route('/oauth/authorize', handler=OAuthAuthorizeHandler, name='oauth-auth'),
    Route('/oauth/callback', handler=OAuthCallbackHandler, name='oauth-callback'),
    Route('/oauth/token', handler=OAuthTokenHandler, name='oauth-token'),
], debug=True, config=configuration)
