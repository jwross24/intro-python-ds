import tweepy
from textblob import TextBlob

# Authenticate
consumer_key = 'hjwLE0Fqf9RkcCHCgpJXeOxwA'
consumer_secret = '43n9FtJvUeTIhRxxlzzhcJgTmazbDpdreH8DCexxPlJsckbDlJ'

access_token = '246975644-to8ejpN6U0ENVJMWzUIP33v8UIH9aBc7R1Tk7Kzs'
access_token_secret = 'CyY1zZPANKJrmwUHreYRrH5mKU81GgchklR3eaMUah4gA'

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
