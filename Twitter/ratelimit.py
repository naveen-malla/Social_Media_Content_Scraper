import tweepy
import time

# Load environment variables from .env file
load_dotenv()

# Get the credentials from environment variables
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Check rate limit status
rate_limit_status = api.rate_limit_status()
remaining = rate_limit_status['resources']['search']['/search/tweets']['remaining']
reset_time_unix = rate_limit_status['resources']['search']['/search/tweets']['reset']

# Convert reset time from Unix timestamp to readable format
reset_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(reset_time_unix))

print(f"Remaining API calls: {remaining}")
print(f"Rate limit resets at: {reset_time}")


# run this code for extra information
#Call the rate_limit_status method on the API object
# limits = api.rate_limit_status()
#
# # Print the remaining limits and reset times for each endpoint
# for category, endpoints in limits['resources'].items():
#     print(category)
#     for endpoint, limit in endpoints.items():
#         print(f'{endpoint}: {limit["remaining"]} out of {limit["limit"]}. Reset at {limit["reset"]}')