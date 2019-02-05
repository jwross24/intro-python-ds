import tweepy
from textblob import TextBlob

consumer_key = 'hjwLE0Fqf9RkcCHCgpJXeOxwA'
consumer_secret = 'XXX'

access_token = '246975644-to8ejpN6U0ENVJMWzUIP33v8UIH9aBc7R1Tk7Kzs'
access_token_secret = 'XXX'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets = api.search('Lambda School')

for tweet in public_tweets:
    print(tweet.text)
    analysis = TextBlob(tweet.text)
    print(analysis.sentiment)
