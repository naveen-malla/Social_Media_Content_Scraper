import os
import pandas as pd
import json
from urllib import request

pd.options.mode.chained_assignment = None  # default='warn'

# code to save images in comments to file system #a9EzXnW a5EAv9O
def dwnld_file_nd_path(post, url, path, index, df):
    if not os.path.isdir("Attachments/" + post): os.makedirs("Attachments/" + post)
    response = request.urlretrieve(url, path)
    df["media_location"].iloc[index] = path
    return df

def save_media(post, file):
    df = pd.read_csv(file, index_col=0)
    df["media_location"] = ""
    attachments = df['attachments']
    for index, attachment in zip(range(0, len(attachments)), attachments):
        if isinstance(attachment, str) and len(
                attachment) > 2 and attachment != 'attachments' and attachment != 'media':
            # print(index, attachment)
            # replacing single quotes with double quotes to convert str to json
            attachment = attachment.replace("'", "\"")
            # converting string to dict using json
            attachment = json.loads(attachment[1:-1])
            # if the attachment has data as key
            if 'data' in attachment.keys():
                # type is animated for gif
                if attachment['data']['type'] == 'ANIMATED':
                    # print(index, attachment['data']['animated']['url'])
                    df = dwnld_file_nd_path(post, attachment['data']['animated']['url'],
                                       "Attachments/" + post + "/" + (file[:-4] + "_" + str(index)) + ".gif", index, df)

                # if there is a large version of image available
                elif 'imageXLarge' in list(attachment['data'].keys()):
                    # print(index, attachment['data']['imageXLarge']['url'])
                    df = dwnld_file_nd_path(post, attachment['data']['imageXLarge']['url'],
                                       "Attachments/" + post + "/" + (file[:-4] + "_" + str(index)) + ".jpg", index, df)

                # downloads the image available at given url
                else:
                    # print(index, attachment['data']['image']['url'])
                    df = dwnld_file_nd_path(post, attachment['data']['image']['url'],
                                       "Attachments/" + post + "/" + (file[:-4] + "_" + str(index)) + ".jpg", index, df)

            # some rows have imageMetaByType as key and not data
            elif 'imageMetaByType' in list(attachment.keys()):
                if attachment['imageMetaByType']['type'] == 'ANIMATED':
                    # print(index, attachment['imageMetaByType']['animated']['url'])
                    df = dwnld_file_nd_path(post, attachment['imageMetaByType']['animated']['url'],
                                       "Attachments/" + post + "/" + (file[:-4] + "_" + str(index)) + ".gif", index, df)
                else:
                    # print(index, attachment['imageMetaByType']['image']['url'])
                    df = dwnld_file_nd_path(post, attachment['imageMetaByType']['image']['url'],
                                       "Attachments/" + post + "/" + (file[:-4] + "_" + str(index)) + ".jpg", index, df)

    # print(df["media_location"])
    df.to_csv(file)