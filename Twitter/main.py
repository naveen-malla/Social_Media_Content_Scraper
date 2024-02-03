import os
import tweepy
from save_media import save_media
from get_data import get_tweets_data
import os
from dotenv import load_dotenv


def get_conversation(tweet_id, client):
    query = 'conversation_id:%s -is:retweet' % tweet_id

    # Create a paginator object with max_results=100
    paginator = tweepy.Paginator(client.search_recent_tweets, query=query,
                                 tweet_fields=['context_annotations', 'created_at'], max_results=100)
    # Create an iterator from the paginator object
    iterator = paginator.flatten()
    return iterator


def get_quotes(tweet_id, client):
    paginator = tweepy.Paginator(client.get_quote_tweets, id=tweet_id, max_results=100,
                                 exclude='retweets')
    # Create an iterator from the paginator object
    iterator = paginator.flatten()
    return iterator


if __name__ == "__main__":
    # Load the environment variables from the .env file
    load_dotenv()

    tweet_id = os.getenv("TWEET_ID")
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
    bearer_token = os.getenv("BEARER_TOKEN")

    # Authenticate with tweepy
    auth = tweepy.OAuth1UserHandler(
        consumer_key, consumer_secret, access_token, access_token_secret
    )
    api = tweepy.API(auth)
    client = tweepy.Client(bearer_token=bearer_token)

    folder = "Replies/" + tweet_id + '_conversation'
    if not os.path.isdir(folder):
        os.makedirs(folder)
    if not os.path.isdir(folder + '/Attachments'):
        os.makedirs(folder + '/Attachments')
    save_media(api, tweet_id, folder + '/Attachments' + '/MainTweetMedia/')

    iterator = get_conversation(tweet_id, client)
    get_tweets_data(tweet_id, iterator, api, folder, "Conversation")

    iterator = get_quotes(tweet_id, client)
    get_tweets_data(tweet_id, iterator, api, folder, "Quotes")
