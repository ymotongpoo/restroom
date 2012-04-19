# -*- coding: utf-8 -*-

from pyoauth2.client import OAuth2AuthorizationFlow


if __name__ == '__main__':
    required_params = {
        'client_id': "QMOIJFCZI4GM3SPTT3JRZI4CAQV40XVW0F2F20YUF2DXGWNB",
        'client_secret': "Q431MFGU1LNMLNIGYIXBQN2FXTQAYXP450G513KC2GSQHC2R",
        'auth_uri': "https://ja.foursquare.com/oauth2/authorize",
        'token_uri': "https://ja.foursquare.com/oauth2/access_token",
        'redirect_uri': "http://www.ymotongpoo.com/"
        }

    extra_auth_params = {
        'response_type': "code",
        }

    extra_token_params = {
        'grant_type': "authorization_code",
        }

    flow = OAuth2AuthorizationFlow(required_params)
    flow.retrieve_authorization_code()
    flow.retrieve_token()
    print flow.access_token
    
