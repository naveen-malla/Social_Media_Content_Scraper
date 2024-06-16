import re

import tweepy
import csv
import textblob
from save_media import savemedia
import os
from dotenv import load_dotenv
import os

tweet_id = "1632199266453311489"


# define a function that takes a sentiment score and returns a label
def sentiment_label(score):
    if score > 0:
        return 'positive'
    elif score < 0:
        return 'negative'
    else:
        return 'neutral'


load_dotenv()  # Load environment variables from .env file

consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
bearer_token = os.getenv("BEARER_TOKEN")
client = tweepy.Client(bearer_token=bearer_token)

# Authenticate with tweepy
auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret, access_token, access_token_secret
)
api = tweepy.API(auth)

filename = tweet_id + '_conversation.csv'
folder = "Replies/" + tweet_id + '_conversation'
if not os.path.isdir(folder):
    os.makedirs(folder)
if not os.path.isdir(folder + '/Attachments'):
    os.makedirs(folder + '/Attachments')
savemedia(api, tweet_id, folder + '/Attachments' + '/MainTweetMedia/')

# Replace with your own conversation id
query = 'conversation_id:%s -is:retweet' % tweet_id

# Create a paginator object with max_results=100
paginator = tweepy.Paginator(client.search_recent_tweets, query=query,
                             tweet_fields=['context_annotations', 'created_at'], max_results=100)

# Create an iterator from the paginator object
iterator = paginator.flatten()

# Open a csv file with write mode
with open(folder + "/" + filename, 'w') as f:
    # Create a csv writer object with fieldnames
    csv_writer = csv.DictWriter(f, fieldnames=(
        'tweet_id',
        'date_time',
        'user',
        'user_name',
        'user_id',
        'user_followers_count',
        'user_friends_count',
        'retweet_count',
        'favorite_count',
        'reply_to_tweet_id',
        'reply_to_user_id',
        'source',
        'coordinates',
        'place',
        'location',
        'language',
        'hashtags',
        'mentions',
        'media_url',
        'media_path',
        'text',
        'sentiment',)
                                )

    # Write the header row to the file
    csv_writer.writeheader()

    # Loop through the iterator until there are no more tweets
    while True:
        try:
            tweet = next(iterator)  # get the next tweet from the iterator

            tweet = api.get_status(tweet.id, tweet_mode="extended")
            tweet = tweet._json

            media_url, media_path = savemedia(api, tweet["id"], folder + '/Attachments/ConversationMedia/')

            print(tweet['full_text'])
            # extract the extra features from each tweet object using its attributes and methods
            tweet_id = tweet["id_str"]
            date_time = tweet["created_at"]
            user = tweet["user"]["screen_name"]
            user_name = tweet["user"]["name"]
            user_id = tweet["user"]["id_str"]
            user_followers_count = tweet["user"]["followers_count"]
            user_friends_count = tweet["user"]["friends_count"]
            retweet_count = tweet["retweet_count"]
            favorite_count = tweet["favorite_count"]
            reply_to_tweet_id = tweet["in_reply_to_status_id_str"]
            reply_to_user_id = tweet["in_reply_to_user_id_str"]
            source = re.search('<.*?>(.*?)<.*?>', tweet["source"]).group(1) # get text from first tag
            coordinates = tweet["coordinates"]  # This might be None
            place = tweet["place"]  # This might be None
            location = tweet["user"]["location"]  # This might be empty string
            language = tweet['lang']
            hashtags = [hashtag['text'] for hashtag in tweet['entities']['hashtags']]  # This might be empty list
            mentions = [mention['screen_name'] for mention in
                        tweet['entities']['user_mentions']]  # This might be empty list
            text = tweet['full_text']
            sentiment = sentiment_label(textblob.TextBlob(text).sentiment.polarity)

            row = {
                'tweet_id': tweet_id,
                'date_time': date_time,
                'user': user,
                'user_name': user_name,
                'user_id': user_id,
                'user_followers_count': user_followers_count,
                'user_friends_count': user_friends_count,
                'retweet_count': retweet_count,
                'favorite_count': favorite_count,
                'reply_to_tweet_id': reply_to_tweet_id,
                'reply_to_user_id': reply_to_user_id,
                'source': source,
                'coordinates': coordinates,
                'place': place,
                'location': location,
                'language': language,
                'hashtags': hashtags,
                'mentions': mentions,
                'media_url': media_url,
                'media_path': media_path,
                'text': text,
                'sentiment': sentiment}

            csv_writer.writerow(row)
        except StopIteration:
            break

    f.close()
