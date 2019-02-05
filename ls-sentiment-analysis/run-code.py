import tweepy
from textblob import TextBlob

# Authenticate
consumer_key = 'XXX'
consumer_secret = 'XXX'

access_token = 'XXX'
access_token_secret = 'XXX'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# Retrieve Tweets
public_tweets = api.search('Lambda School')

for tweet in public_tweets:
    print(tweet.text)

    # Perform sentiment analysis on Tweets
    analysis = TextBlob(tweet.text)
    print(analysis.sentiment)
    print()
