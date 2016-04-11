import os
import tweepy
import simplejson as json
import csv
import pprint
from utils import flatten_json 
from kitchen.text.converters import getwriter, to_bytes
import sys


UTF8Writer = getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

# Read in all API keys from environment
consumer_key = os.environ['TWITTER_CONSUMER_KEY']
consumer_secret = os.environ['TWITTER_CONSUMER_SECRET_KEY']
access_token = os.environ['TWITTER_ACCESS_KEY']
access_token_secret = os.environ['TWITTER_ACCESS_SECRET_KEY']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# u'Mon Apr 11 16:57:05 +0000 2016'


# override tweepy.StreamListener to add logic 
class MyStreamListener(tweepy.StreamListener):
  def __init__(self,outfile):
    ''' Assigns string of the raw output filename '''
    self.outfile = outfile
    self.tweet_counter = 0
    self.tweet_cap = 25

  def on_data(self, data):
    # Twitter returns data in JSON format - we need to decode it first
    decoded = json.loads(data)

    # Flatten the json with appropriate naming 
    out_dict = flatten_json(decoded)
    print(out_dict.keys())
    if self.tweet_counter == 0:
      write_csv_file(self.outfile, out_dict.keys(), mode='overwrite')

    write_csv_file(self.outfile, out_dict.values())

    self.tweet_counter += 1
    if self.tweet_counter < self.tweet_cap:
      return True
    else:
      # terminate when appropriate
      return False 


def get_tweets(filters):
  '''Creates a stream and applies filters'''
  # creates a stream
  myStreamListener = MyStreamListener('streamed_tweets.txt')
  myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener) 

  # starts a stream
  myStream.filter(track=filters)


def write_csv_file(output_csv, out_list, mode='append'):
  modes = {'append':'a','overwrite':'w'}
 
  out_list_ascii = [s.encode('ascii', 'replace').replace('\n',' ') 
      for s in out_list]
  with open(output_csv, modes.get(mode,'a')) as csvfile:
    tweetwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    tweetwriter.writerow(out_list_ascii)


if __name__ == '__main__':
  get_tweets(['chicken','Nashville']) 
