import csv
import os
import datetime
from textblob import TextBlob
from praw import Reddit
from praw.models import MoreComments
import pandas as pd
from transformers import BertForSequenceClassification, AutoTokenizer
from openpyxl.workbook import Workbook
from dotenv import load_dotenv
import os

# Load environment variables from .env file
def get_credentials():
    load_dotenv()  
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    password = os.getenv("PASSWORD")
    user_agent = os.getenv("USER_AGENT")
    username = os.getenv("USERNAME")
    return client_id, client_secret, password, user_agent, username

# This function takes in the body of a comment and uses the TextBlob library to determine if the sentiment is
# positive, neutral, or negative.
def calculate_sentiment(body):
    analysis = TextBlob(body)
    if analysis.sentiment.polarity > 0:
        return "Positive"
    elif analysis.sentiment.polarity == 0:
        return "Neutral"
    else:
        return "Negative"

# This function takes in a post URL and uses the credentials obtained from the get_credentials function to authenticate
# with the Reddit API and scrape the comments from the specified post. The comments are then saved to a CSV file with a
# sentiment column added.
def scrape_comments(post_url):
    client_id, client_secret, password, user_agent, username = get_credentials()
    reddit = Reddit(client_id=client_id,
                    client_secret=client_secret,
                    password=password,
                    user_agent=user_agent,
                    username=username)
    submission = reddit.submission(url=post_url)
    submission.comments.replace_more(limit=None)
    comments_file = f"{submission.subreddit}_{submission.id}_comments.csv"
    print("Authentication Successful")
    if not os.path.isdir("Comments"):
        os.makedirs("Comments")
    file = open(f"{os.getcwd()}/{'Comments'}/{comments_file}", "w")
    writer = csv.writer(file)
    writer.writerow(["Author",
                     "Body",
                     "Created Time",
                     "Id",
                     "Parent_id",
                     "Permalink",
                     "Score",
                     "Sentiment"])
    comment_queue = submission.comments[:]
    while comment_queue:
        comment = comment_queue.pop(0)
        if isinstance(comment, MoreComments):
            for comment in comment.comments():
                try:
                    created_utc = comment.created_utc
                    date_time = datetime.datetime.utcfromtimestamp(created_utc).strftime('%Y-%m-%d %H:%M:%S')
                    sentiment = calculate_sentiment(comment.body)
                    writer.writerow([comment.author.name,
                                     comment.body,
                                     date_time,
                                     comment.id,
                                     comment.parent_id,
                                     comment.permalink,
                                     comment.score,
                                     sentiment])
                except:
                    continue
                comment_queue.extend(comment.replies)
        else:
            try:
                created_utc = comment.created_utc
                date_time = datetime.datetime.utcfromtimestamp(created_utc).strftime('%Y-%m-%d %H:%M:%S')
                sentiment = calculate_sentiment(comment.body)
                writer.writerow([comment.author.name,
                                 comment.body,
                                 date_time,
                                 comment.id,
                                 comment.parent_id,
                                 comment.permalink,
                                 comment.score,
                                 sentiment])
            except:
                pass
        comment_queue.extend(comment.replies)
    print("Comments saved!!!")
    print("Added Sentiment column to", comments_file)
    file.close()

    # read the csv file and save it as an excel file
    df = pd.read_csv(f"{os.getcwd()}/{'Comments'}/{comments_file}")
    excel_file = f"{submission.subreddit}_{submission.id}_comments.xlsx"
    df.to_excel(f"{os.getcwd()}/{'Comments'}/{excel_file}", index=False)

    return excel_file

# This function takes in the comments file and uses the BERT model and tokenizer from the transformers library to
# classify the sentiment of the comments in the file.
def bert_sentiment(comments_file):

    # Instantiate BERT model and tokenizer
    model = BertForSequenceClassification.from_pretrained("bert-base-cased")
    tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")

    # Read csv file
    df = pd.read_csv("Comments/" + comments_file)
    print(df.head())
    # Add new column to store BERT sentiment
    df["BERTSentiment"] = ""

    for index, row in df.iterrows():
        text = row["Body"]
        input_ids = tokenizer.encode(text, return_tensors="pt")
        sentiment = model(input_ids)[0]
        sentiment = sentiment.argmax().item()

        if sentiment == 0:
            df.at[index, "BERTSentiment"] = "Negative"
        elif sentiment == 1:
            df.at[index, "BERTSentiment"] = "Neutral"
        elif sentiment == 2:
            df.at[index, "BERTSentiment"] = "Positive"

    df.to_csv(comments_file)
    return comments_file



if __name__ == '__main__':
    post_url = "https://www.reddit.com/r/chess/comments/10wpqoc/lichess_1577_rated_puzzle_how_quickly_were_you/"
    comments_file = scrape_comments(post_url)
    #comments_file = bert_sentiment(comments_file)


