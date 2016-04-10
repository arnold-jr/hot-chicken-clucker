import os
import tweepy
import simplejson as json
import csv

# Read in all API keys from environment
consumer_key = os.environ['TWITTER_CONSUMER_KEY']
consumer_secret = os.environ['TWITTER_CONSUMER_SECRET_KEY']
access_token = os.environ['TWITTER_ACCESS_KEY']
access_token_secret = os.environ['TWITTER_ACCESS_SECRET_KEY']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# override tweepy.StreamListener to add logic 
class MyStreamListener(tweepy.StreamListener):
  def __init__(self,outfile):
    ''' Assigns string of the raw output filename '''
    self.outfile = outfile
    self.records = []
    self.tweet_counter = 0
    self.tweet_cap = 25

  def on_data(self, data):
    # Twitter returns data in JSON format - we need to decode it first
    decoded = json.loads(data)

    # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by 
    # users
    self.records.extend([
        decoded['text'].encode('ascii', 'ignore').replace('\n',' ')])
    print(self.records[-1])
    self.tweet_counter += 1

    if self.tweet_counter < self.tweet_cap:
      return True
    else:
      with open(self.outfile, 'wb') as outfile:
        outfile.write('\n'.join(self.records))
      return False


def get_tweets(filters):
  '''Creates a stream and applies filters'''
  # creates a stream
  myStreamListener = MyStreamListener('streamed_tweets.txt')
  myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener) 

  # starts a stream
  myStream.filter(track=filters)


def write_csv_file(output_csv):
  with open(output_csv, 'wb') as csvfile:
    tweetwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    tweetwriter.writerow(['tweet'] * 5 + ['Baked Beans'])
    tweetwriter.writerow(['tweet', 'Lovely tweet', 'Wonderful tweet'])

if __name__ == '__main__':
  get_tweets(['Bernie','Hillary']) 
  write_csv_file('eggs.csv')
