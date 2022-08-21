from get_comments import save_comments
from save_attachments import save_media
from sentiment_score import get_senti_score

# a5EAv9O a9EzXnW
if __name__ == "__main__":
    post = "a9EzXnW"

    print("\nSaving comments and replies\n")
    comments_file, replies_file = save_comments(post)
    print("\nComment and replies saved")

    print("\n===============================================\n")
    print("Saving media in comments and replies")
    save_media(post, comments_file)
    save_media(post, replies_file)
    print("Saving media done")

    print("\n===============================================\n")
    print("Getting sentiment scores for comments and replies")
    get_senti_score(comments_file)
    get_senti_score(replies_file)
    print("Sentiment Scores Obtained")


