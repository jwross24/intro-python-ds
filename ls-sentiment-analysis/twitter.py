import numpy as np
import operator
import tweepy
import datetime as DT
from textblob import TextBlob


# Step 1 - Authenticate
consumer_key = 'CONSUMER_KEY_HERE'
consumer_secret = 'CONSUMER_SECRET_HERE'

access_token = 'ACCESS_TOKEN_HERE'
access_token_secret = 'ACCESS_TOKEN_SECRET_HERE'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# Step 2 - Prepare query features

# List of bootcamps with 
bootcamps = ['Sarkozy', 'Kosciusko', 'Cope', 'Juppe', 'Fillon', 'Le Maire',
             'Poisson']
# Set default until_date to today, since_date to a week before
until_date = DT.date().today()
since_date = until_date - DT.timedelta(days=7)


# Step 2b - Label the sentiments
def get_label(analysis, threshold=0):
    if analysis.sentiment[0] > threshold:
        return 'Positive'
    elif analysis.sentiment[0] == threshold:
        return 'Neutral'
    else:
        return 'Negative'


# Step 3 - retrieve Tweets and save them
all_polarities = {}
for bootcamp in bootcamps:
    this_bootcamp_polarity = []
    # Get tweets about the bootcamp between the dates
    this_bootcamp_tweets = api.search(q=bootcamp, count=100, since=since_date,
                                      until=until_date)
    # Save the Tweets in a CSV
    with open('%s_tweets.csv' % bootcamp, 'wb') as this_bootcamp_file:
        this_bootcamp_file.write('tweet,sentiment_label\n')
        for tweet in this_bootcamp_tweets:
            analysis = TextBlob(tweet.text)
            # Get the label corresponding to the sentiment
            this_bootcamp_polarity.append(analysis.sentiment[0])
            this_bootcamp_file.write('%s,%s\n' % (tweet.text.encode('utf8'),
                                                  get_label(analysis)))
    # Save the mean for final results
    all_polarities[bootcamp] = np.mean(this_bootcamp_polarity)

# Step bonus - Print a Result
sorted_analysis = sorted(all_polarities.items(), key=operator.itemgetter(1),
                         reverse=True)
print('Mean Sentiment Polarity in descending order :')
for candidate, polarity in sorted_analysis:
    print('%s : %0.3f' % (candidate, polarity))
