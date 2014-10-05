from __future__ import absolute_import
#from celery import shared_task
#from celery.task.schedules import crontab
#from celery.decorators import periodic_task
#from celery.utils.log import get_task_logger

import feedparser
import time
import phone_messenger as msg
import pickle
import blpapi
import numpy as np

from textblob import TextBlob
from tickerwatch.models import UserProfile, Stock
from sklearn import svm, preprocessing, decomposition
from query_ticker_data import queryData


def moving_average(a, n=3):
  retval = []
  for i in xrange(n-1, len(a)):
    retval.append(0.0)
    for j in xrange(n):
      retval[-1] += a[i-j]
    retval[-1] /= n
  return retval


def test(model, ticker):
  ticker_data = queryData(ticker)
  if not ticker_data or len(ticker_data) < 4:
    return None

  ticker_data = moving_average(ticker_data)

  scaler = model['scaler']
  clf = model['classifier']

  rss_url = 'http://finance.yahoo.com/rss/headline?s=%s' % ticker
  feed = feedparser.parse(rss_url)
  if not feed['items']:
    return None

  avg_sent = 0.0
  max_act = 1
  best_story = None
  for item in feed['items']:
    blob = TextBlob(item['title'])
    sent = blob.sentiment.polarity

    X = np.array([[sent] + ticker_data[-4:]])
    scaler.transform(X)
    z = clf.predict(X)

    if abs(z[0]) > max_act:
      max_act = z[0]
      best_story = TextBlob(item['title'])

  return best_story



SLEEP_TIME = 60 # seconds

stocks = Stock.objects.all()
tickers = []
for stock in stocks:
  tickers.append(stock.ticker)
f = open('data/model.pickle')
model = pickle.load(f)
f.close()

while(True):
  for ticker in tickers:
    story = test(model, ticker)
    if not story:
      continue

    users = Stock.objects.get(ticker=ticker).users
    users = [UserProfile.objects.get(user__id=user.id) for user in users.all()]
    numbers = [user.phone_number for user in users]
    for number in numbers:
      print number
      # Replace this number with the number from Users for not demo
      try:
        msg.send_text(number, 'att', story)
      except:
        continue
  time.sleep(SLEEP_TIME)


#@periodic_task(run_every=(crontab(hour="*", minute="*", day_of_week="*")))
#def query_cycle():
#  logger.info("Start query cycle")
#  counter = 0
#  counter += 1
#
#  ticker = 'FB'
#  rss_url = 'http://finance.yahoo.com/rss/headline?s=%s' % ticker
#  feed = feedparser.parse(rss_url)
#  for item in feed['items']:
#    item['title']
#
#  message = "OMGROFL"
#  msg.send_text('5103886932', 'att', message)


