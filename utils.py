import urlparse

import feedparser
import requests
from feedgen.feed import FeedGenerator
from lxml import etree


def get_title_for_url(url):
    try:
        response = requests.get(url)
        root = etree.HTML(response.text)
        return root.find(".//title").text
    except:
        return ""


def filter_fb_rss_feeed(fb_notifications_feed_url):
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
