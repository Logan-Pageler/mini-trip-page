import functools
import json
import os

from flask import Flask, render_template, url_for, redirect, session
from authlib.integrations.flask_client import OAuth
from flask_cors import CORS, cross_origin
import os


AUTH_REDIRECT_URI = os.environ.get("FN_AUTH_REDIRECT_URI", default=False)
BASE_URI = os.environ.get("FN_BASE_URI", default=False)
CLIENT_ID = os.environ.get("FN_CLIENT_ID", default=False)
CLIENT_SECRET = os.environ.get("FN_CLIENT_SECRET", default=False)
CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'

app = Flask(__name__)
app.secret_key = os.urandom(12)

CORS(app, support_credentials=True)

oauth = OAuth(app)
oauth.register(
    name='google',
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  print('test')
  return response

@app.route('/auth/')
def index():
    # if google_auth.is_logged_in():
    #     user_info = google_auth.get_user_info()
    #     return '<div>You are currently logged in as ' + user_info['given_name'] + '<div><pre>' + json.dumps(user_info, indent=4) + "</pre>"

    return session.get('token') if session.get('token') != None else 'You are not currently logged in.'

@app.route('/auth/Login/')
def google():


    
    return oauth.google.authorize_redirect(AUTH_REDIRECT_URI).get_data()
    # return uri

@app.route('/auth/google/callback/')
@cross_origin(supports_credentials=True)
def google_auth():
    token = oauth.google.authorize_access_token()
    session['token'] = token
    
    print(" Google User ", token)
    return redirect('http://localhost:3000?token=' + token['userinfo']['at_hash'] + '&name=' + token['userinfo']['name'])

@app.route('/auth/getToken/')
def get_token():
    return session.get('token') if session.get('token') != None else 'false'
    