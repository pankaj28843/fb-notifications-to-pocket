import hashlib
import urlparse

import feedparser
import requests
from feedgen.feed import FeedGenerator
from lxml import etree

from cache import pylibmc_client

TITLES_FOR_ERROR_PAGES = [
    '301 moved permanently',
    '302 found',
    '303 see other',
    '307 temporary redirect',
    '400 bad request',
    '401 authorization required',
    '402 payment required',
    '403 forbidden',
    '404 not found',
    '405 not allowed',
    '406 not acceptable',
    '409 conflict',
    '410 gone',
    '411 length required',
    '412 precondition failed',
    '413 request entity too large',
    '415 unsupported media type',
    '416 requested range not satisfiable',
    '400 request header or cookie too large',
    '400 the ssl certificate error',
    '400 no required ssl certificate was sent',
    '400 the plain http request was sent to https port',
    '500 internal server error',
    '501 not implemented',
    '502 bad gateway',
    '503 service temporarily unavailable',
    '507 insufficient storage'
]


def generate_key_for_text(text):
    return hashlib.sha512(text).hexdigest()


def fetch_title_for_url(url):
    try:
        response = requests.get(url)
        root = etree.HTML(response.text)
        title = root.find(".//title").text
        if title.lower().strip() in TITLES_FOR_ERROR_PAGES:
            return None
        return title
    except:
        return None


def get_title_for_url(url):
    key = generate_key_for_text(url)
    # get from cache
    title = pylibmc_client.get(key)

    if title is None:
        title = fetch_title_for_url(url)
        pylibmc_client.set(key, title, time=172800)

    return title


def _filter_fb_rss_feeed(fb_notifications_feed_url):
    parsed_feed = feedparser.parse(fb_notifications_feed_url)
    filtered_entries = filter(
        lambda x: ' shared a link: "' in x.title, parsed_feed.entries)

    fg = FeedGenerator()
    fg.id('https://fb-notifications-to-pocket.herokuapp.com/')
    fg.title('Facebook Notifications to Pocket')
    fg.author({'name': 'Pankaj Singh', 'email': 'psjinx@gmail.com'})
    fg.description(
        '''Filter FB notifications which contain a link and generate a new rss feed which will be used by IFTTT''')
    fg.link(href='https://fb-notifications-to-pocket.herokuapp.com/')

    for entry in filtered_entries:
        root = etree.HTML(entry.summary_detail.value)
        title = entry.title.split(" shared a link: ")[1].strip()[1:-2]
        author_name = entry.title.split(" shared a link: ")[0].strip()
        url = urlparse.parse_qs(
            urlparse.urlparse(root.findall(".//a")[-1].attrib["href"]).query)["u"][0]

        title = get_title_for_url(url) or title

        fe = fg.add_entry()
        fe.id(entry.id)
        fe.link(href=url)
        fe.published(entry.published)
        fe.author({'name': author_name})
        fe.title(title)

    return fg.atom_str(pretty=True)


def filter_fb_rss_feeed(fb_notifications_feed_url):
    key = generate_key_for_text(fb_notifications_feed_url)
    # get from cache
    atom_str = pylibmc_client.get(key)

    if atom_str is None:
        atom_str = _filter_fb_rss_feeed(fb_notifications_feed_url)
        pylibmc_client.set(key, atom_str, time=60)

    return atom_str
