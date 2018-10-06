"""Subrequest example."""

from flask import Flask, Response, request, make_response, render_template
from urllib.parse import urlparse, parse_qs


app = Flask(__name__)


AUTH_PARAM_NAME = '__auth'


@app.route('/app')
def index():
    """Index."""
    return """
    <!doctype html>
    <html>
    <head>
        <title>Nginx Subrequests Example</title>
    </head>
    <body>
        <div class="content">
            <p>Try me!!</p>
            <video src="http://localhost:8080/media/test_vid_hd.mp4?__auth=1" type="video/mp4" controls="controls" width="300"
       height="200">Video not supported</video>

            <video src="http://localhost:8080/media/test_vid_hd.mp4" type="video/mp4" controls="controls" width="300"
       height="200">Video not supported</video>
        </div>
    </body>
    </html>
    """


@app.route('/auth')
def auth():
    """Authorize some times."""
    original_url = request.headers.get('x-original-uri', None)

    auth_cookie = request.cookies.get(AUTH_PARAM_NAME, None)
    if auth_cookie is None:
        auth_cookie = request.args.get(AUTH_PARAM_NAME, None)
    if auth_cookie is None and original_url is not None:
        o = urlparse(original_url)
        qs = parse_qs(o.query)
        auth_cookie = qs.get(AUTH_PARAM_NAME, None)
    if auth_cookie is None:
        return Response('Unauthorized', 401)

    return Response('OK', 200)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
