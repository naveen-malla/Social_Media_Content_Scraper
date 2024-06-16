import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

post="aMEEpeA"
# chrome_options = Options()
# chrome_options.headless = True

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
    if post in video_link:
        print('video_link:', video_link)
        r = requests.get(video_link, allow_redirects=True)
        open("Attachments/" + post + "/" + "Meme.mp4", 'wb').write(r.content)

    else:
        image_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "//div[@class='post-container']/div[1]/a/div/picture/img"))).get_attribute('src')
        print('image_link: ', image_link)
        r = requests.get(image_link, allow_redirects=True)
        open("Attachments/" + post + "/" + "Meme.jpg", 'wb').write(r.content)
except:
    image_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, "//div[@class='post-container']/div[1]/a/div/picture/img"))).get_attribute('src')
    if post in image_link:
        print('image_link: ', image_link)
        r = requests.get(image_link, allow_redirects=True)
        open("Attachments/" + post + "/" + "Meme.jpg", 'wb').write(r.content)
    else:
        video_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "//div[@class='post-container']/div[1]/a/div/video/source[3]"))).get_attribute('src')
        print('video_link:', video_link)
        r = requests.get(video_link, allow_redirects=True)
        open("Attachments/" + post + "/" + "Meme.mp4", 'wb').write(r.content)

print("Meme Downloaded.")
driver.quit()
