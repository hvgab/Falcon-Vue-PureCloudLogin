import base64
import os
import uuid

import falcon
import requests
from falcon_cors import CORS

cors = CORS(allow_all_origins=True, allow_all_methods=True, allow_credentials_all_origins=True)

# falcon.ResponseOptions.secure_cookies_by_default = False
app = falcon.API(middleware=[cors.middleware])
app.resp_options.secure_cookies_by_default = False

sessions = dict()


class CookiePrinter(object):
    """docstring"""
    def on_get(self, req, resp):
        print('cookies:')
        cookies = req.cookies
        sessionid = cookies['sessionid']
        if sessionid in sessions:
            print('sessionid in sessions')
            session = sessions[sessionid]
        else:
            print('sessionid not in sessions')
            session = dict()

        resp.media = dict(cookies = cookies, session = session)


class Auth(object):
    """docstring for Auth."""

    def on_get(self, req, resp):
        print('Auth get')
        print()
        redirect_url = f'https://login.mypurecloud.ie/oauth/authorize?client_id={os.getenv("PCP_CLIENT_ID")}&response_type=code&redirect_uri=http://localhost:5000/oauth/callback'
        resp.media = dict(redirect_to=redirect_url)


class AuthCallback(object):
    def on_get(self, req, resp):
        print(req.params)

        if 'code' in req.params:
            # get access token
            PCP_CLIENT_ID = os.getenv('PCP_CLIENT_ID')
            PCP_CLIENT_SECRET = os.getenv('PCP_CLIENT_SECRET')
            auth64 = base64.b64encode(
                f'{PCP_CLIENT_ID}:{PCP_CLIENT_SECRET}'.encode('ascii'))
            urlquery = dict(
                grant_type='authorization_code',
                code=req.params['code'],
                redirect_uri='http://localhost:5000/oauth/callback')
            headers = dict(Authorization=b'Basic ' + auth64)
            r = requests.post(
                'https://login.mypurecloud.ie/oauth/token',
                data=urlquery,
                headers=headers)

            print(r.status_code)
            print(r.text)
            print(r.json())
            resp.media = r.json()

            access_token = r.json()['access_token']
            token_type = r.json()['token_type']
            expires_in = r.json()['expires_in']

            me_url = 'https://api.mypurecloud.ie/api/v2/users/me'
            headers = dict(Authorization='Bearer ' + access_token)
            person = requests.get(me_url, headers=headers)
            resp.media = person.json()

            print('lager en sessionid')
            sessionid = str(uuid.uuid4())
            print(f'sessionid: {sessionid}')
            resp.set_cookie('sessionid', sessionid, path='/')
            print('sessionid satt i cookies')

            print('legger til session i sessions')
            sessions[sessionid] = dict(user=person.json())
            print('session lagt til:')
            print(sessions)

            print('redirect to frontend')
            raise falcon.HTTPSeeOther('http://localhost:8080')

        else:
            resp.media = dict(idk='idk')


class AuthVerifyCode(object):
    """ Trenger ikke denne? """
    def on_get(self, req, resp):
        print('auth verify code')
        print(req)
        print(resp)


app.add_route('/oauth/purecloud/login', Auth())
app.add_route('/oauth/callback', AuthCallback())
app.add_route('/cookieprinter', CookiePrinter())
