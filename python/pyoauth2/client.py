# -*- coding: utf-8 -*-

__author__ = "Yoshifumi YAMAGUCHI <@ymotongpoo>"

__all__ = ['OAuth2AuthenticationFlow']

import requests

from urllib import urlencode
import json
import os
import webbrowser
try:
    import cPickle as Pickle
except Exception:
    import Pickle


REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'



class OAuth2AuthorizationFlow(object):
    """ OAuth 2.0 authorization class
    """

    def __init__(self, required_params,
                 extra_auth_params=None,
                 extra_token_params=None,
                 **kwargs):

        """
        Args:
          required_params: dictionary including required parameters
        """
        self.client_id = required_params['client_id']
        self.client_secret = required_params['client_secret']
        self.auth_uri = required_params['auth_uri']
        self.token_uri = required_params['token_uri']
        self.redirect_uri = required_params['redirect_uri']

        if extra_auth_params:
            self._extra_auth_params = extra_auth_params
        else:
            self._extra_auth_params = {}

        if extra_token_params:
            self._extra_token_params = extra_token_params
        else:
            self._extra_token_params = {}
        
        self.params = {}
        self.params.update(kwargs)

        if 'scope' in self.params:
            self.scope = ' '.join(self.params['scope'])

        self.authorization_code = None
        self.access_token = None


    def retrieve_authorization_code(self):
        """ retrieve authorization code to get access token
        """
        
        request_param = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": self._extra_token_params.get('response_type', "code"),
            "access_type": 'offline'
            }

        if self._extra_auth_params:
            request_param.update(self._extra_auth_params)

        params = urlencode(request_param)
        r = requests.get(self.auth_uri, params=request_param,
                         allow_redirects=False)
        
        url = r.headers.get('location')
        print url
        webbrowser.open_new_tab(url)

        authorization_code = raw_input("Code: ")
        if self.validate_code(authorization_code):
            self.authorization_code = authorization_code

        
    def retrieve_token(self):
        """ retrieve access token with code fetched via 
        retrieve_authorization_code method.
        """

        if self.authorization_code:
            request_param = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "redirect_uri": self.redirect_uri,
                "code": self.authorization_code,
                "grant_type": 'authorization_code'
                }

            if self._extra_token_params:
                request_param.update(self._extra_token_params)

            content_length = len(urlencode(request_param))
            request_param['content-length'] = str(content_length)

            r = requests.get(self.token_uri, params=request_param,
                             allow_redirects=True)
            self.access_token = json.loads(r.text)

        else:
            print "authorization code is required before getting accesss token"
            print "Please call retrieve_authorization_code() beforehand"



    def validate_code(self, code):
        return True
