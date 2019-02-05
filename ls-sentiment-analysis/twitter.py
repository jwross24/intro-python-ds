import os
import re
import tweepy
from textblob import TextBlob


class TwitterClient(object):
    '''
    Generic Twitter Class for the App
    '''
    def __init__(self, query, retweets_only=False, with_sentiment=False):
        # Keys and tokens from the Twitter Dev Console
        consumer_key = os.environ['CONSUMER_KEY']
        consumer_secret = os.environ['CONSUMER_SECRET']
        access_token = os.environ['ACCESS_TOKEN']
        access_token_secret = os.environ['ACCESS_TOKEN_SECRET']

        # Attempt authentication
        try:
            self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.query = query
            self.retweets_only = retweets_only
            self.with_sentiment = with_sentiment
            self.api = tweepy.API(self.auth)
            self.tweet_count_max = 100  # To prevent rate limiting
        except Exception:
            print('Error: Authentication Failed')
            raise

    # Set the query to search for on Twitter
    def set_query(self, query=''):
        self.query = query

    # Set if we should count Retweets or not
    def set_retweet_checking(self, retweets_only='false'):
        self.retweets_only = retweets_only

    # Set if we should record the sentiment of a Tweet or not
    def set_with_sentiment(self, with_sentiment='false'):
        self.with_sentiment = with_sentiment

    # Clean the tweet according to the regex rule
    def clean_tweet(self, tweet):
        rule = '(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)'
        return ' '.join(re.sub(rule, ' ', tweet).split())

    # Get the overall sentiment of the tweet
    def get_tweet_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    # Search Twitter for the Tweets to find the sentiment of
    def get_tweets(self):
        tweets = []

        try:
            recd_tweets = self.api.search(q=self.query,
                                          count=self.tweet_count_max)
            if not recd_tweets:
                pass
            for tweet in recd_tweets:
                parsed_tweet = {}
                ttext = tweet.text

                parsed_tweet['text'] = ttext
                parsed_tweet['user'] = tweet.user.screen_name

                if self.with_sentiment == 1:
                    parsed_tweet['sentiment'] = self.get_tweet_sentiment(ttext)
                else:
                    parsed_tweet['sentiment'] = 'unavailable'

                if tweet.retweet_count > 0 and self.retweets_only == 1:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                elif not self.retweets_only:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)

            return tweets

        except tweepy.TweepError as e:
            print('Error : ' + str(e))
