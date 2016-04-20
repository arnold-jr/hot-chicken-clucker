import sys
from kitchen.text.converters import getwriter, to_bytes
import os
from requests_oauthlib import OAuth1
import requests
import simplejson as json
from utils import flatten_json 
import pandas as pd

# Sets system out to print unicode
UTF8Writer = getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)


def get_n_tweets(n_tweets,track):
  """Returns 100 of the most recent tweets from Twitter's API."""
  auth = get_twitter_auth()
  return get_twitter_data(auth,n_tweets,track)

def get_twitter_auth():
  '''Returns a Twitter auth object'''
  # Reads in all API keys from environment
  try:
    consumer_key = os.environ['TWITTER_CONSUMER_KEY']
    consumer_secret = os.environ['TWITTER_CONSUMER_SECRET_KEY']
    access_token = os.environ['TWITTER_ACCESS_KEY']
    access_token_secret = os.environ['TWITTER_ACCESS_SECRET_KEY']
  except KeyError:
    print("Please set twitter authentication environment variables.")
    raise

  # create an auth object
  auth = OAuth1(
      consumer_key, 
      consumer_secret,
      access_token,
      access_token_secret
  )
  return auth 


# u'Mon Apr 11 16:57:05 +0000 2016'
def get_twitter_data(auth,n_tweets,track):
  """ Pulls some data from twitter's sample streaming API
  
  Args:
      auth: An OAuth1 object
      n_tweets: Number of tweets in a chunk
      track: List of keyword terms for filtering
  Returns: 
      n_tweets of the most recent 'sample' tweets.
  """

  # prepare the hdf store


  params = {'track':','.join(track),
            'language':'en'} 
  r_stream = requests.get(
    'https://stream.twitter.com/1.1/statuses/filter.json',
    auth=auth, stream=True,
    params=params
  )
  counter = 0
  tweets = [dict()]*n_tweets
  for line in r_stream.iter_lines():
    # filter out keep-alive new lines
    if not line:
      continue
    
    tweet = json.loads(line)
    
    #only want substantive tweets
    if 'text' not in tweet:
      continue
    
    print(tweet['text'])

    tweets[counter] = flatten_json(tweet)

    counter +=1
    if counter % 10 == 0:
      print(pd.DataFrame.from_records(tweets))
    if counter >= n_tweets:
      break

  print(tweet)
  print(flatten_json(tweet))

  return tweets


if __name__ == '__main__':
  get_n_tweets(100,['hot chicken','Nashville chicken','KFC','chicken'])
