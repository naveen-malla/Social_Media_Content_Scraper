import tweepy
from dotenv import dotenv_values

# Load the environment variables from the .env file
env_vars = dotenv_values()

# Get the value of bearer_token from the environment variables
bearer_token = env_vars.get("bearer_token")

client = tweepy.Client(bearer_token=bearer_token)

# Replace the limit=1000 with the maximum number of Tweets you want
paginator = tweepy.Paginator(client.get_quote_tweets, id=1632199266453311489, max_results=100,
                              exclude='retweets')
# Create an iterator from the paginator object
iterator = paginator.flatten()

while True:
    try:
        tweet = next(iterator)  # get the next tweet from the iterator
        print(tweet)
    except StopIteration:
        break