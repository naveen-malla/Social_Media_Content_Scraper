import requests
import os


def save_media(api, tweet_id, path):
    tweet = api.get_status(tweet_id, tweet_mode="extended")
    if "media" in tweet.entities:
        if not os.path.isdir(path):
            os.makedirs(path)
        for media in tweet.extended_entities["media"]:
            # print(media)
            if media['type'] == 'video' or media['type'] == 'animated_gif':
                media_url = media['video_info']['variants'][0]['url']
                filename = str(tweet_id) + ".mp4"

            elif media['type'] == 'photo':
                media_url = media['media_url']
                filename = str(tweet_id) + ".jpg"
            # print(media_url)

            response = requests.get(media_url)
            with open(path + filename, "wb") as f:
                f.write(response.content)
        return media_url, (path + filename)
    else:
        return "", ""
