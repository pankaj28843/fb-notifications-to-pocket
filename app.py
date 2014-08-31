import os
import urllib

from flask import Flask, request, Response, render_template
from utils import filter_fb_rss_feeed


app = Flask(__name__)


@app.route('/')
def home():
    fb_feed_url = request.args.get('u', '').strip()
    encoded_fb_feed_url = urllib.urlencode({"u": fb_feed_url})

    if fb_feed_url:
        if not fb_feed_url.startswith("https://"):
            raise ValueError("Need a secure URL.")
        if not fb_feed_url.startswith("https://www.facebook.com/feeds/notifications.php?id="):
            raise ValueError("Need a valid FB notifications rss feed url.")

    return render_template('home.html', fb_feed_url=fb_feed_url, encoded_fb_feed_url=encoded_fb_feed_url)


@app.route('/feed')
def filter_fb_feed():
    fb_feed_url = request.args.get('u', '')
    if not fb_feed_url:
        raise ValueError("URL can't be empty")
    if not fb_feed_url.startswith("https://"):
        raise ValueError("Need a secure URL.")
    if not fb_feed_url.startswith("https://www.facebook.com/feeds/notifications.php?id="):
        raise ValueError("Need a valid FB notifications rss feed url.")

    xml = filter_fb_rss_feeed(fb_feed_url)
    return Response(response=xml,
                    status=200,
                    mimetype="application/rss+xml")


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
