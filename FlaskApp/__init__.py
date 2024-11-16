import json
import time

import os
import pathlib
import requests

from flask import Flask, session, redirect, request, abort, render_template
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
from .config import config

from . import my_db

db = my_db.db

app = Flask(__name__)
app.secret_key = config.get("APP_SECRET_KEY")

app.config['SQLALCHEMY_DATABASE_URI'] = config.get('SQLALCHEMY_DATABASE_URI')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

GOOGLE_CLIENT_ID = (
    config.get("GOOGLE_CLIENT_ID")
)
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, ".client_secret.json")


flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=[
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "openid",
    ],
    redirect_uri="https://sd3biot.online/callback",
)

alive = 0
data = {}


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/protected_area")
@login_is_required
def protected_area():
    my_db.add_user_and_login(session['name'], session['google_id'])
    return render_template("protected_area.html", user_id=session['google_id'], online_users=my_db.get_all_logged_in_users(), admin_id=config.get('GOOGLE_ADMIN_ID'))


@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route("/logout")
def logout():
    my_db.user_logout(session['google_id'])
    session.clear()
    return redirect("/")


@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # States don't match

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token, request=token_request, audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    print(session["google_id"])
    print(session["name"])
    return redirect("/protected_area")


@app.route("/keep_alive")
def keep_alive():
    global alive, data
    alive += 1
    keep_alive_count = str(alive)
    data["keep_alive"] = keep_alive_count
    parsed_json = json.dumps(data)
    print(parsed_json)
    return str(parsed_json)


@app.route('/grant-<user_id>-<read>-<write>', methods=["POST"])
def grant_access(user_id, read, write):
    if session['google_id']:
        if session['google_id'] == config.get('GOOGLE_ADMIN_ID'):
            print(f"Admin granting {user_id}-{read}-{write}")
            my_db.add_user_permission(user_id, read, write)
            if read=="true" and write=="true":
                




if __name__ == "__main__":
    app.run()
