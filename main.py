import requests
import cloudscraper
from bs4 import BeautifulSoup
import json
import pandas as pd
import os


def getMemeData(memes):
    data = []
    for url in memes:
        scraper = cloudscraper.create_scraper()
        html = scraper.get(url)
        if html.status_code == 200:
            soup = BeautifulSoup(html.content, 'html.parser')
        else:
            print("Unable to fetch page. Status Code:", html.status_code)
        title = soup.find('title').text[:-7]
        votes = soup.find('meta', property='og:description')['content'].split(' ')[0]
        comments = soup.find('meta', property='og:description')['content'].split(' ')[3]
        votes = int(votes) if len(votes) <= 3 else int("".join(votes.split(',')))
        comments = int(comments) if len(comments) <= 3 else int("".join(comments.split(',')))
        data.append([url, title, votes, comments])
    meme_data = pd.DataFrame(data, columns=['Meme_URL', 'Title', 'UpVotes', 'Comments'])
    meme_data.to_csv("Memes.csv", index=False, header=True)


if __name__ == "__main__":
    memes = ["https://9gag.com/gag/a5EAv9O", "https://9gag.com/gag/aqjO7xR", "https://9gag.com/gag/aRXGGYj",
             "https://9gag.com/gag/av5wGB5", "https://9gag.com/gag/av5q61Z", "https://9gag.com/gag/a9EzXnW",
             "https://9gag.com/gag/aWjp2n2"]
    getMemeData(memes)

#
# def getUrl():
#     html = requests.get('https://9gag.com/')
#     if html.status_code == 200:
#         soup = BeautifulSoup(html.text, 'html.parser')
#     else:
#         print("Unable to fetch page. Status Code:", html.status_code)
#         return
#     div = soup.find(type='application/ld+json')
#     json_obj = json.loads(div.text.strip())
#     url_list = json_obj['itemListElement']
#     memes = []
#     for data in url_list:
#         memes.append(data['url'])
#     return memes
#
#
# def getMemeData(memes):
#     data = []
#     for url in memes:
#         scraper = cloudscraper.create_scraper()
#         html = scraper.get(url)
#         if html.status_code == 200:
#             soup = BeautifulSoup(html.content, 'html.parser')
#         else:
#             print("Unable to fetch page. Status Code:", html.status_code)
#         title = soup.find('title').text[:-7]
#         votes = soup.find('meta', property='og:description')['content'].split(' ')[0]
#         comments = soup.find('meta', property='og:description')['content'].split(' ')[3]
#         print(votes, comments)
#         #votes = int(votes) if len(votes) <= 3 else int("".join(votes.split(',')))
#         #comments = int(comments) if len(comments) <= 3 else int("".join(votes.split(',')))
#         data.append([url, title, votes, comments])
#     meme_data = pd.DataFrame(data, columns=['Meme_URL', 'Title', 'UpVotes', 'Comments'])
#     if os.path.exists("Memes.csv"):
#         #print(meme_data['Title'])
#         csv_data = pd.read_csv("Memes.csv")
#         csv_urls = csv_data['Meme_URL'].tolist()
#         for i in range(0, len(csv_urls)):
#             print(len(meme_data))
#             for j in range(0, len(meme_data)):
#                 if csv_urls[i] == memes[j]:
#                     # print(memes[i], csv_urls[j])
#                     # print(meme_data.iloc[i]['Title'], "||||", csv_data.iloc[j]['Title'])
#                     csv_data.iloc[i] = meme_data.loc[meme_data['Meme_URL'] == memes[j]]
#                     #csv_data.iloc[i] = meme_data.iloc[j]
#                     #meme_data = meme_data.drop(meme_data.index[[j]])
#                     meme_data = meme_data.drop(meme_data.loc[meme_data['Meme_URL'] == memes[j]])
#                     meme_data = meme_data.reset_index(drop=True)
#                     break
#         #print(len(meme_data))
#         csv_data = pd.concat([csv_data, meme_data])
#         csv_data.to_csv("Memes.csv", index=False, header=True)
#     else:
#         meme_data.to_csv("Memes.csv", index=False, header=True)
#
#
# if __name__ == "__main__":
#     memes = getUrl()
#     print(memes)
#     getMemeData(memes)
