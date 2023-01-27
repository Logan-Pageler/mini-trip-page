import functools
import json
import os

from flask import Flask, render_template, url_for, redirect, session, request
from authlib.integrations.flask_client import OAuthError, OAuth
import pymysql
import os
from flask_cors import CORS



AUTH_REDIRECT_URI = os.environ.get("FN_AUTH_REDIRECT_URI", default=False)
BASE_URI = os.environ.get("FN_BASE_URI", default=False)
CLIENT_ID = os.environ.get("FN_CLIENT_ID", default=False)
CLIENT_SECRET = os.environ.get("FN_CLIENT_SECRET", default=False)
CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'

DB_HOST = os.environ.get("DB_HOST", default=False)
DB_USERNAME = os.environ.get("DB_USERNAME", default=False)
DB_PASSWORD = os.environ.get("DB_PASSWORD", default=False)
DB_NAME = os.environ.get("DB_NAME", default=False)
DB_PORT = int(os.environ.get("DB_PORT", default=False))

db = pymysql.connect(host=DB_HOST, user=DB_USERNAME, password=DB_PASSWORD, db=DB_NAME, port=DB_PORT)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_ENDPOINT", default=False)
app.secret_key = os.urandom(12)

cors = CORS(app, origins=["http://localhost:3000"], headers=['Content-Type'], expose_headers=['Access-Control-Allow-Origin'], supports_credentials=True)


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

# allow access from origin
# @app.after_request
# def after_request(response):
#   response.headers.add('Access-Control-Allow-Origin', '*')
#   response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#   response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
#   return response

@app.route('/auth/login/')
def google():

    response = oauth.google.authorize_redirect(AUTH_REDIRECT_URI)
    print(response.headers.get('Location'))
    # response.headers.add('Access-Control-Allow-Origin', '*')
    # response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    # response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')

    session['test'] = 'test'
    return response.headers.get('Location')

@app.route('/auth/callback/')
def google_auth():
    print(session['test'])
    token = oauth.google.authorize_access_token()
    session['token'] = token
    
    print(" Google User ", token)
    return 'http://localhost:3000?token=' + token['userinfo']['email'] + '&name=' + token['userinfo']['name']



@app.route('/api/getTable/')
def get_table():
    
    if('token' in session.keys()):
        user = session['token']['userinfo']['email']
        cur = db.cursor()
        cur.execute('SELECT user_table FROM User_Data WHERE user = %s', user)
        result = cur.fetchone()
        if result == None:
            return 'false'
        print(result[0])
        return result[0]

    return 'false'

@app.route('/api/setTable/', methods=['POST'])
def set_table():
    if('token' in session.keys()):
        cur = db.cursor()
        print(cur.execute('''
            REPLACE INTO User_Data (user, user_table) VALUES (%s, %s)
        ''', (session['token']['userinfo']['email'], request.data)))

        db.commit()
    
        return 'true'
    return 'false'
        


    