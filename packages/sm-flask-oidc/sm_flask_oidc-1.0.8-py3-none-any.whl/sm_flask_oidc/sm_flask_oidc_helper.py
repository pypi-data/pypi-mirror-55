import  flask
import base64
import hashlib
import os
import re
import urllib.parse
import requests


class SmFlaskOidcHelper:
    """
    You have to create a the bellow routes:
        login-callback
        logout-callback

    You have to set app.secret_key for flask.session 
    
    params:
        CLIENT_ID 
        CLIENT_SECRET
        APP_URI
        AUTH_API_ROUTE
        AUTH_STATE
        
    The following keys will be stored in the session: id_token, name, email and is_authorized
    
    """
    def __init__(self, client_id, clint_scret, app_uri, auth_api_route, auth_state, login_callback_route = "/", logout_callback_route = "/"):
        if app_uri.endswith('/') == False:
            app_uri = app_uri + '/'
        self.CLIENT_ID = client_id
        self.CLIENT_SECRET = clint_scret
        self.LOGIN_REDIRECT_URI = app_uri + 'login-callback'
        self.LOGOUT_REDIRECT_URI = app_uri + 'logout-callback'
        self.AUTH_API_ROUTE = auth_api_route
        self.AUTH_STATE = auth_state
        self.LOGIN_CALLBACK_ROUTE = login_callback_route
        self.LOGOUT_CALLBACK_ROUTE = logout_callback_route

    # helpers -----------------------------------------------
    # def _b64_decode(data):
    #     data += '=' * (4 - len(data) % 4)
    #     return base64.b64decode(data).decode('utf-8')

    # def jwt_payload_decode(jwt):
    #     _, payload, _ = jwt.split('.')
    #     return json.loads(_b64_decode(payload))

    # def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())
    # def json2obj(data): return json.loads(data, object_hook=_json_object_hook)
    def is_success_status_code(self, status_code): return status_code >= 200 and status_code < 300
    # -------------------------------------------------------


    def login(self):
        flask.session["is_authorized"] = False
        code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode('utf-8')
        code_verifier = re.sub('[^a-zA-Z0-9]+', '', code_verifier)
        flask.session["code_verifier"] = code_verifier
        
        code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
        code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8')
        code_challenge = code_challenge.replace('=', '')

        authorizeBaseUrl = self.AUTH_API_ROUTE + "/connect/authorize"
        authorizeParams = {
            "response_type": "code",
            "client_id": self.CLIENT_ID,
            "scope": "openid profile",
            "redirect_uri": self.LOGIN_REDIRECT_URI,
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
            "state": self.AUTH_STATE
        }
        
        authorizeUrl = authorizeBaseUrl + '?' + urllib.parse.urlencode(authorizeParams, True)
        return flask.redirect(authorizeUrl)

    def login_callback(self):
        url_query = urllib.parse.urlparse(flask.request.url).query
        redirect_params = urllib.parse.parse_qs(url_query)
        auth_code = redirect_params['code'][0]
        auth_state = redirect_params['state'][0]
        if auth_state != self.AUTH_STATE:
            return 'It seems that the call was hacked by CSRF other related attacks.', 412  # This protects against CSRF and other related attacks.
        code_verifier = flask.session.get("code_verifier")
        flask.session["code_verifier"] = None

        # get token :: exchanges the authorization code by an access token
        resp = requests.post(
            url = self.AUTH_API_ROUTE + "/connect/token",
            data={
                "grant_type": "authorization_code",
                "client_id": self.CLIENT_ID,
                "client_secret": self.CLIENT_SECRET,
                "redirect_uri": self.LOGIN_REDIRECT_URI,
                "code": auth_code,
                "code_verifier": code_verifier,
            },
            allow_redirects = False,
            verify = False
        )

        if self.is_success_status_code(resp.status_code) == False:
            return f'Request Failed. Message: {resp.text}', resp.status_code

        result = resp.json()
        flask.session["id_token"] = result['id_token']

        print('StatusCode: ' + str(resp.status_code))

        userinfo_resp = requests.get(self.AUTH_API_ROUTE + "/connect/userinfo",
            headers = {
                'authorization': "Bearer " + result['access_token'],
                'content-type': "application/json"
            }, 
            verify = False,
            allow_redirects = False
        )
        
        if self.is_success_status_code(userinfo_resp.status_code) == False:
            return f'Request Failed. Message: {userinfo_resp.text}', userinfo_resp.status_code

        user_info = userinfo_resp.json()

        name = ''
        email = ''
        try:
            name = user_info['name'][0]
            email = user_info['name'][1]
        except:
            name = user_info.name

        flask.session["name"] = name
        flask.session["email"] = email
        flask.session["is_authorized"] = True

        return flask.redirect(self.LOGIN_CALLBACK_ROUTE)


    def logout(self):
        id_token = flask.session["id_token"]
        endsessionBaseUrl = self.AUTH_API_ROUTE + "/connect/endsession"
        authorizeParams = {
            "id_token_hint": id_token,
            "post_logout_redirect_uri ": self.LOGOUT_REDIRECT_URI,
            "state": self.AUTH_STATE
        }
        endsessionUrl = endsessionBaseUrl + '?' + urllib.parse.urlencode(authorizeParams, True)
        return flask.redirect(endsessionUrl)

    def logout_callback(self):
        flask.session["id_token"] = None
        flask.session["name"] = None
        flask.session["email"] = None
        flask.session["is_authorized"] = False
        
        return flask.redirect(self.LOGOUT_CALLBACK_ROUTE)