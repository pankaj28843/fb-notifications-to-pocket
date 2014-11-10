import os
import urllib

from flask import Flask, render_template, request, Response
from utils import filter_fb_rss_feeed, transform_twitrss_feed_to_link_feed

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



@app.route('/get-links-from-twitter-feed')
def get_links_from_twitter_feed():
    twitrss_feed_url = request.args.get('u', '')
    if not twitrss_feed_url:
        raise ValueError("URL can't be empty")
    if not twitrss_feed_url.startswith("http://"):
        raise ValueError("Need a secure URL.")
    if not twitrss_feed_url.startswith("http://twitrss.me/twitter_user_to_rss"):
        raise ValueError("Need a valid TwitRSS url for twitter user.")

    xml = transform_twitrss_feed_to_link_feed(twitrss_feed_url)
    return Response(response=xml,
                    status=200,
                    mimetype="application/rss+xml")


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
