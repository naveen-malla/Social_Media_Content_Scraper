
import requests
import cloudscraper
from bs4 import BeautifulSoup
import json
import pandas as pd
import os
import selenium
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc

if __name__ == '__main__':

    options = Options()
    # options.headless = True
    driver = uc.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.maximize_window()
    driver.get("https://9gag.com/gag/a5EAv9O")
    prev_h = 0
    for i in range(30):
        height = driver.execute_script("""
                   function getActualHeight() {
                       return Math.max(
                           Math.max(document.body.scrollHeight, document.documentElement.scrollHeight),
                           Math.max(document.body.offsetHeight, document.documentElement.offsetHeight),
                           Math.max(document.body.clientHeight, document.documentElement.clientHeight)
                       );
                   }
                   return getActualHeight();
               """)
        driver.execute_script(f"window.scrollTo({prev_h},{prev_h + 200})")
        time.sleep(1)
        prev_h += 200
        if prev_h >= height:
            break
    time.sleep(5)
    title = driver.title[:-7]
    try:
        upvotes_count = driver.find_element(By.XPATH, "//meta[@property='og:description']").get_attribute("content").split(' ')[0]
        comments_count = driver.find_element(By.XPATH, "//meta[@property='og:description']").get_attribute("content").split(' ')[3]
        upvotes_count = int(upvotes_count) if len(upvotes_count) <= 3 else int("".join(upvotes_count.split(',')))
        comments_count = int(comments_count) if len(comments_count) <= 3 else int("".join(comments_count.split(',')))
        date_posted = driver.find_element(By.XPATH, "//p[@class='message']")
        date_posted = date_posted.text.split("·")[1].strip()
        # actions = ActionChains(driver)
        # link = driver.find_element(By.XPATH, "//button[@class='comment-list__load-more']")
        # actions.move_to_element(link).click(on_element=link).perform()
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.comment-list__load-more"))).click()
        print([my_elem.text for my_elem in driver.find_elements(By.CSS_SELECTOR, "div.comment-list-item__text")])
        #driver.implicitly_wait(15)

        # element = driver.find_element(By.XPATH,
        #                               "//div[@class='vue-recycle-scroller ready page-mode direction-vertical']")
        #
        # print(element.text)
        driver.quit()
    except NoSuchElementException or Exception as err:
        print(err)

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
#         #print(votes, comments)
#         #votes = int(votes) if len(votes) <= 3 else int("".join(votes.split(',')))
#         #comments = int(comments) if len(comments) <= 3 else int("".join(votes.split(',')))
#         data.append([url, title, votes, comments])
#     meme_data = pd.DataFrame(data, columns=['Meme_URL', 'Title', 'UpVotes', 'Comments'])
#     if os.path.exists("Memes.csv"):
#         csv_data = pd.read_csv("Memes.csv")
#         csv_urls = csv_data['Meme_URL'].tolist()
#         for i in range(0, len(csv_urls)):
#             for j in range(0, len(meme_data)):
#                 if csv_urls[i] == memes[j]:
#                     # print(memes[i], csv_urls[j])
#                     # print(meme_data.iloc[i]['Title'], "||||", csv_data.iloc[j]['Title'])
#                     csv_data.iloc[i] = meme_data.iloc[j]
#                     meme_data = meme_data.drop(meme_data.index[[j]])
#                     meme_data = meme_data.reset_index(drop=True)
#                     break
#         csv_data = pd.concat([csv_data, meme_data])
#         csv_data.to_csv("Memes.csv", index=False, header=True)
#     else:
#         meme_data.to_csv("Memes.csv", index=False, header=True)
#
#
# if __name__ == "__main__":
#     memes = getUrl()
#     #print(memes)
#     getMemeData(memes)
