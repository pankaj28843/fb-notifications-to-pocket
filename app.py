import os
from flask import Flask, request, Response

from utils import filter_fb_rss_feeed

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello World!'


@app.route('/feed')
def filter_fb_feed():
    url = request.args.get('u', '')
    if not url.startswith("https://"):
        raise ValueError("Need a secure URL.")
    if not url.startswith("https://www.facebook.com/feeds/notifications.php?id="):
        raise ValueError("Need a valid FB notifications rss feed url.")

    xml = filter_fb_rss_feeed(url)
    return Response(response=xml,
                    status=200,
                    mimetype="application/rss+xml")


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
