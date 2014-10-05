from __future__ import absolute_import
from celery import shared_task
import feedparser
import time
import phone_messenger as msg


SLEEP_TIME = 60 # seconds


def query_cycle():
  counter = 0
  while(True):
    counter += 1

    ticker = 'FB'
    rss_url = 'http://finance.yahoo.com/rss/headline?s=%s' % ticker
    feed = feedparser.parse(rss_url)
    for item in feed['items']:
      item['title']

    msg.send_text('5103886932', 'att', message)
    time.sleep(SLEEP_TIME)


