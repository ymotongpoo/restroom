# -*- coding: utf-8 -*-

from pyoauth2.client import OAuth2AuthorizationFlow, FileStorage, OAuth2APIRequest

if __name__ == '__main__':

    fsq_venue_uri = r"https://api.foursquare.com/v2/users/self/venuehistory"

    required_params = {
        'client_id': "QMOIJFCZI4GM3SPTT3JRZI4CAQV40XVW0F2F20YUF2DXGWNB",
        'client_secret': "Q431MFGU1LNMLNIGYIXBQN2FXTQAYXP450G513KC2GSQHC2R",
        'auth_uri': "https://ja.foursquare.com/oauth2/authorize",
        'token_uri': "https://ja.foursquare.com/oauth2/access_token",
        'redirect_uri': "http://www.ymotongpoo.com/"
        }

    extra_auth_params = {
        'response_type': "code",
        'access_type': "offline"
        }

    extra_token_params = {
        'grant_type': "authorization_code",
        }

    storage = FileStorage('foursquare.dat')
    credentials = storage.get()
    if credentials is None:
        flow = OAuth2AuthorizationFlow(required_params,
                                   extra_auth_params,
                                   extra_token_params)
        flow.retrieve_authorization_code()
        credentials = flow.retrieve_token()
        storage.save(credentials)
    
    access_token = credentials['access_token']

    req = OAuth2APIRequest(access_token)
    data = req.request(fsq_venue_uri)
    print data

    
    
