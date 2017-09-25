from uuid import uuid4
from os import environ
from flask import Flask
app = Flask(__name__)

app.config.update(
    CLIENT_ID=environ['SPOTIFY_CLIENT_ID'],
    CLIENT_SECRET=environ['SPOTIFY_CLIENT_SECRET'],
    )
app.secret_key = str(uuid4())

import spotify_flask_web_api.views
