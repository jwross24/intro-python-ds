import csv
import datetime as DT
import operator
import re
import tweepy

from numpy import mean
from textblob import TextBlob


# Step 1 - Authenticate
consumer_key = 'CONSUMER_KEY_HERE'
consumer_secret = 'CONSUMER_SECRET_HERE'

access_token = 'ACCESS_TOKEN_HERE'
access_token_secret = 'ACCESS_TOKEN_SECRET_HERE'

try:
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)
    tweet_count_max = 45  # to prevent rate limiting
except Exception:
    print('Error: authentication failed')
    raise


# Clean the Tweet according to the regex rule
def clean_tweet(tweet):
    pattern = '(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)'
    return ' '.join(re.sub(pattern, ' ', tweet).split())


# Label the sentiments
def get_label(polarity, threshold=0):
    if polarity > threshold:
        return 'Positive'
    elif polarity == threshold:
        return 'Neutral'
    else:
        return 'Negative'


# Set default until_date to today, since_date to 3 days before
until_date = DT.date.today()
until_fmt = until_date.strftime('%Y-%m-%d')

since_date = until_date - DT.timedelta(days=3)
since_fmt = since_date.strftime('%Y-%m-%d')


def get_tweets(query, retweets_only=False, with_sentiment=True,
               since_date=since_fmt, until_date=until_fmt):
    tweets = []
    polarities = []

    try:
        # Read in the Tweets from Twitter API
        recd_tweets = tweepy.Cursor(api.search, q=[query, 'bootcamp'],
                                    tweet_mode='extended', since=since_fmt,
                                    until=until_fmt).items(tweet_count_max)
        if not recd_tweets:
            pass

        # Parse Tweets for content and user
        for tweet in recd_tweets:
            parsed_tweet = {}

            parsed_tweet['text'] = tweet.full_text
            parsed_tweet['user'] = tweet.user.screen_name

            # Add sentiments to the Tweet data
            if with_sentiment:
                analysis = TextBlob(clean_tweet(tweet.full_text))
                polarity = analysis.sentiment.polarity
                polarities.append(polarity)
                parsed_tweet['sentiment'] = get_label(polarity)
            else:
                parsed_tweet['sentiment'] = 'N/A'

            # Retweet handler
            if tweet.retweet_count > 0 and retweets_only:
                if parsed_tweet not in tweets:
                    tweets.append(parsed_tweet)
            elif not retweets_only:
                if parsed_tweet not in tweets:
                    tweets.append(parsed_tweet)

        return tweets, polarities

    except tweepy.TweepError as e:
        print('Error:', str(e))


# Output the Tweet, author, and sentiment label to CSV
def write_tweets_to_csv(bootcamp, tweets):
    with open('%s_tweets.csv' % bootcamp, 'w', newline='') as f:
        field_names = ['text', 'user', 'sentiment']
        writer = csv.DictWriter(f, fieldnames=field_names)

        writer.writeheader()
        for tweet in tweets:
            writer.writerow(tweet)


# List of bootcamps
bootcamps = ['Le Wagon', 'Ironhack', 'App Academy', 'General Assembly',
             'Bloc', 'Thinkful', 'Flatiron School', 'HackerYou',
             'Coding Dojo', 'The Tech Academy', 'Hack Reactor', 'Actualize',
             'Lambda School', 'Tech Talent South', 'Epicodus',
             'Startup Institute', 'Codesmith', 'Makers Academy',
             'Brain Station', 'Fullstack Academy']
all_polarities = {}

# Loop through the bootcamps, get Tweets and polarities
for bootcamp in bootcamps:
    tweets, polarities = get_tweets(bootcamp)
    write_tweets_to_csv(bootcamp, tweets)
    # Calculate mean polarity for each bootcamp
    if polarities:
        all_polarities[bootcamp] = mean(polarities)

# Print the average sentiments in descending order
if all_polarities:
    sorted_polarities = sorted(all_polarities.items(),
                               key=operator.itemgetter(1), reverse=True)
    print()
    print('Mean sentiment polarity in descending order:')
    for bootcamp, polarity in sorted_polarities:
        print('%s: %0.3f' % (bootcamp, polarity))
    print()
