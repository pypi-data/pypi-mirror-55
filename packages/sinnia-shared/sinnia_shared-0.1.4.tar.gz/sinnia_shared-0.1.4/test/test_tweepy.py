import sys, os, logging, requests, copy
#reload(sys)
#sys.setdefaultencoding('utf-8')

import re
import string
import tweepy

from datetime import time, timedelta, datetime, tzinfo, date

if sys.path[0] + '/../../../' not in sys.path:
    sys.path.append(sys.path[0] + '/../../../')
if sys.path[0] + '/../../' not in sys.path:
    sys.path.append(sys.path[0] + '/../../')

def omdb_request(by, term, item_type, year=None):
  #type=[movie, series, episode]
  url = "http://www.omdbapi.com/"

  payload = {'apikey': '9919030a',
             'r': 'json',
             'type': item_type,
             'page': '1',    # For by_search
             'plot': 'full'} # For by_title
  if (by == 'search'): payload['s'] = term 
  if (by == 'title'):  payload['t'] = term 
  if (year != None): payload['year'] = year
  print('Params: %s' % payload)
  r = requests.get('%s'%(url), params=payload)
  print('Status code: %s' % r.status_code)
  if r.status_code == 400 or r.status_code != 200:
    print('Status: %s...' % r.status_code)
    return False
  if not r.encoding:
    r.encoding = 'utf-8'
  print('Json as text: %s...' % r.text)
  return r.json()


def tw_rate_limit_status():
  consumer_key = "ej4tiAWGeTWWrzR33MrQA"
  consumer_secret = "OQ7qQ3ciSMbAgr2O1N6JCgQTAElgRnHT2a5qZggNI8g"
  acc_token_4 = "323895533-aC5G4O2FF3nH5Gdt6Al4v5IwqeHZTKjcvEl3I3KX"
  acc_token_secret_4 = "OAcYb4m5SXCwigvnFz7xhzQSRNsYzKtxI6HRWpPGk"
  acc_token_12 = "524581668-7QztehEFOwJ7FjXhu5UDOeh6mqMtp1uAv7XN5hF8"
  acc_token_secret_12 = "0DlZ04SObdwZG2p3nBOcM7hyZCOL0lEThFzS0qYaEE"

  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(acc_token_12, acc_token_secret_12)
  api = tweepy.API(auth)

  resp = api.rate_limit_status()
  print(resp)
    

if __name__ == '__main__':
  #tw_rate_limit_status()
  omdb_request('title', 'It','movie',2017)
