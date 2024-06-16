import csv
import praw
import pandas as pd
from textblob import TextBlob
import datetime

import csv
import os
from datetime import datetime
from praw.models import MoreComments
import os
from dotenv import load_dotenv
import os

def scrape_comments(post_url):
    load_dotenv()  # Load environment variables from .env file

    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        password=os.getenv("REDDIT_PASSWORD"),
        user_agent=os.getenv("REDDIT_USER_AGENT"),
        username=os.getenv("REDDIT_USERNAME"),
    )
    submission = reddit.submission(url=post_url)
    submission.comments.replace_more(limit=None)
    comments_file = f"{submission.subreddit}_{submission.id}_comments.csv"
    file = open(os.path.join(os.getcwd(), comments_file), "w")
    writer = csv.writer(file)
    writer.writerow(["author", "body", "created_utc", "id", "parent_id", "permalink", "score", "Sentiment"])

    comment_queue = submission.comments[:]
    while comment_queue:
        comment = comment_queue.pop(0)
        if isinstance(comment, MoreComments):
            for comment in comment.comments():
                try:
                    created_utc = comment.created_utc
                    date_time = datetime.utcfromtimestamp(created_utc).strftime('%Y-%m-%d %H:%M:%S')
                    sentiment = TextBlob(comment.body).sentiment.polarity
                    if sentiment > 0:
                        sentiment = "Positive"
                    elif sentiment < 0:
                        sentiment = "Negative"
                    else:
                        sentiment = "Neutral"
                    writer.writerow([comment.author, comment.body, date_time, comment.id, comment.parent_id, comment.permalink, comment.score,  sentiment])
                except:
                    continue
                comment_queue.extend(comment.replies)
        else:
            try:
                created_utc = comment.created_utc
                date_time = datetime.utcfromtimestamp(created_utc).strftime('%Y-%m-%d %H:%M:%S')
                sentiment = TextBlob(comment.body).sentiment.polarity
                if sentiment > 0:
                    sentiment = "Positive"
                elif sentiment < 0:
                    sentiment = "Negative"
                else:
                    sentiment = "Neutral"
                writer.writerow([comment.author, comment.body, date_time, comment.id, comment.parent_id, comment.permalink, comment.score, sentiment])
            except:
                pass
            comment_queue.extend(comment.replies)

    return comments_file

def add_sentiment_to_csv(csv_file):
    df = pd.read_csv(csv_file)
    df["Sentiment"] = df["body"].apply(lambda x: TextBlob(x).sentiment.polarity)
    df.to_csv(csv_file, index=False)
    print("Sentiment analysis performed and added to: ", csv_file)

if __name__ == "__main__":
    post_url = "https://www.reddit.com/r/HistoryMemes/comments/9uboug/this_subs_controversial_rn/"
    comments_file = scrape_comments(post_url)
    add_sentiment_to_csv(comments_file)
