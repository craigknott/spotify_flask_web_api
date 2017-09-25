import requests
import urllib

from uuid import uuid4
from flask import render_template, request, redirect, jsonify, session

from spotify_flask_web_api import app

CLIENT_ID = app.config['CLIENT_ID']
CLIENT_SECRET = app.config['CLIENT_SECRET']
RESPONSE_TYPE = 'code'
STATE_KEY = 'spotify_auth_state'
REDIRECT_URI = 'http://localhost:5000/callback'
SCOPE = 'user-read-private user-read-email'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    state = str(uuid4())
    session[STATE_KEY] = state
    params = {
        'client_id': CLIENT_ID,
        'response_type': RESPONSE_TYPE,
        'redirect_uri': REDIRECT_URI,
        'scope': SCOPE,
        'state': state
    }
    return redirect('https://accounts.spotify.com/authorize?' + urllib.urlencode(params))


@app.route('/callback', methods=['GET'])
def callback():
    code = request.args.get('code')
    state = request.args.get('state')
    stored_state = session.get(STATE_KEY)
    if state is None or state != stored_state:
        return redirect('/#?error=state_mismatch')

    r = requests.post('https://accounts.spotify.com/api/token',
                      params={
                          'code': code,
                          'redirect_uri': REDIRECT_URI,
                          'grant_type': 'authorization_code',
                          'client_id': CLIENT_ID,
                          'client_secret': CLIENT_SECRET
                      },
                      headers={'Content-Type': 'application/x-www-form-urlencoded'})
    r.raise_for_status()
    session['access_token'] = r.json().get('access_token')
    session['refresh_token'] = r.json().get('refresh_token')

    # use the access token to access the Spotify Web API
    r = requests.get('https://api.spotify.com/v1/me', headers={'Authorization': 'Bearer ' + session['access_token']})
    r.raise_for_status()
    return jsonify(r.json())
