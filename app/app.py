"""Subrequest example."""

from flask import Flask, Response, request, make_response, render_template, redirect, url_for, session, abort
from urllib.parse import urlparse
import string
from random import randint, choice


RANDOM_CHAR_CHOICES = string.ascii_letters + string.digits


app = Flask(__name__)
app.secret_key = "l\xd3Z\x85\xbd ;R;\xbb'\xe3\xd5\x17\x9e\xfb"

SITE_URL = 'https://demos.kountanis.com/app'


AUTH_PARAM_NAME = '__auth'
valid_tokens = set()


@app.before_request
def csrf_protect():
    if request.method == "POST":
        token = session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(403)


def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = generate_token()
    return session['_csrf_token']


app.jinja_env.globals['csrf_token'] = generate_csrf_token

def generate_token():
    return "".join(choice(RANDOM_CHAR_CHOICES) for x in range(8))

@app.route('/app')
def index():
    """Index."""
    logged_in = request.cookies.get(AUTH_PARAM_NAME, None) is not None
    res = make_response(render_template('index.html', logged_in=logged_in))
    return res


@app.route('/login', methods=('POST',))
def login():
    token = request.cookies.get(AUTH_PARAM_NAME, None)
    if token is None:
        token = generate_token()
        if token not in valid_tokens:
            valid_tokens.add(token)
    res = make_response(redirect('https://demos.kountanis.com/app'))
    res.set_cookie(AUTH_PARAM_NAME, token)
    return res

@app.route('/logout', methods=('POST',))
def logout():
    res = make_response(redirect('https://demos.kountanis.com/app'))
    res.set_cookie(AUTH_PARAM_NAME, '', expires=0)
    return res


@app.route('/auth')
def auth():
    """Authorize using cookie."""
    original_url = request.headers.get('x-original-uri', None)

    auth_cookie = request.cookies.get(AUTH_PARAM_NAME, None)
    if auth_cookie is None:
        return Response('Unauthorized', 401)
    if auth_cookie not in valid_tokens:
        return Response('Unauthorized', 401)

    return Response('OK', 200)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
