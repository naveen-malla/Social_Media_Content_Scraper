import os
import pandas as pd
import json
from urllib import request
import requests
#from undetected_chromedriver._compat import ChromeDriverManager

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

pd.options.mode.chained_assignment = None  # default='warn'

# function to save the meme file
def save_meme(post):

    # Creating a webdriver instance
    driver = webdriver.Chrome(ChromeDriverManager().install())
    url = 'https://9gag.com/gag/' + post
    print('url:', url)
    driver.get(url)

    if not os.path.isdir("Attachments/" + post):
        os.makedirs("Attachments/" + post)

    try:
        video_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "//div[@class='post-container']/div[1]/a/div/video/source[3]"))).get_attribute('src')
        print('video_link:', video_link)
        r = requests.get(video_link, allow_redirects=True)
        open("Attachments/" + post + "/" + "Meme.mp4", 'wb').write(r.content)

    except:
        try:
            image_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "//div[@class='post-container']/div[1]/a/div/picture/img"))).get_attribute('src')
            print('image_link: ', image_link)
            r = requests.get(image_link, allow_redirects=True)
            open("Attachments/" + post + "/" + "Meme.jpg", 'wb').write(r.content)
        except:
            pass

    driver.quit()

# code to save images in comments to file system #a9EzXnW a5EAv9O
def dwnld_file_nd_path(post, url, path, index, df):
    response = request.urlretrieve(url, path)
    df["media_location"].iloc[index] = path
    return df

def save_media(post, file):
    if not os.path.isdir("Attachments/" + post): os.makedirs("Attachments/" + post)
    try:
        df = pd.read_csv(file, index_col=0)
        df["media_location"] = ""
        attachments = df['attachments']
        for index, attachment in zip(range(0, len(attachments)), attachments):
            if isinstance(attachment, str) and len(
                    attachment) > 2 and "'type': 'userMedia'" in attachment:
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
    except:
        pass
