from get_comments import save_comments
from save_attachments import save_media
from sentiment_score import get_senti_score

# a5EAv9O a9EzXnW
if __name__ == "__main__":
    post = "a9EzXnW"

    # comments_file, replies_file = save_comments(post)
    #
    # save_media(post, comments_file)
    # save_media(post, replies_file)
    #
    # get_senti_score(comments_file)
    #get_senti_score(replies_file)
    get_senti_score("a9EzXnW_comments.csv")


