import csv
from email.mime import image
from re import T
from tkinter import SCROLL, Image
from unittest import result
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc

if __name__ == '__main__':
    options = Options()
    # options.headless = True
    driver = uc.Chrome(version_main=102)
    driver.maximize_window()
    driver.get("https://9gag.com/gag/a5EAv9O")
    time.sleep(5)

    # click on I accept cookies
    actions = ActionChains(driver)
    try:
        consent_button = driver.find_element(By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]')
        actions.move_to_element(consent_button).click().perform()
    except:
        pass

    for i in range(31):
        actions.click()
        actions.send_keys(Keys.ARROW_DOWN).perform()
    time.sleep(4)

    # getting meta data
    try:
        title = driver.title[:-7]
        try:
            upvotes_count = \
            driver.find_element(By.XPATH, "//meta[@property='og:description']").get_attribute("content").split(' ')[0]
            upvotes_count = int(upvotes_count) if len(upvotes_count) <= 3 else int("".join(upvotes_count.split(',')))
        except:
            pass
        try:
            comments_count = \
            driver.find_element(By.XPATH, "//meta[@property='og:description']").get_attribute("content").split(' ')[3]
            comments_count = int(comments_count) if len(comments_count) <= 3 else int(
                "".join(comments_count.split(',')))
        except:
            pass
        try:
            date_posted = driver.find_element(By.XPATH, "//p[@class='message']")
            date_posted = date_posted.text.split("·")[1].strip()
        except:
            pass
    except:
        pass

    time.sleep(3)

    # click on fresh comments section
    fresh_comments = driver.find_element(By.XPATH, '//*[@id="page"]/div[1]/section[2]/section/header/div/button[2]')
    actions.move_to_element(fresh_comments).click(on_element=fresh_comments).perform()
    time.sleep(5)

    # click on lood more comments button to load all the comments
    fresh_comments = driver.find_element(By.CSS_SELECTOR, '.comment-list__load-more')
    actions.move_to_element(fresh_comments).click(on_element=fresh_comments).perform()

    miN = 1000
    results = []
    comments = {}
    while miN <= 20000:
        window = 'window.scrollTo(0,' + str(miN) + ')'
        driver.execute_script(window)
        time.sleep(3)

        # Dealing with all comments
        try:
            # Scrape the main comments
            try:
                All_comments = driver.find_elements(By.CSS_SELECTOR, "div.vue-recycle-scroller__item-view")
            except:
                All_comments = driver.find_elements(By.CSS_SELECTOR, "div.vue-recycle-scroller__item-view")

            del_comm_cnt = 1
            for item in All_comments:
                try:
                    html = item.get_attribute("innerHTML")
                    if "comment-list-item__text" in html:
                        comment = item.find_element(By.CSS_SELECTOR, "div.comment-list-item__text").text
                    elif "comment-list-item__deleted-text" in html:
                        comment = item.find_element(By.CSS_SELECTOR, "div.comment-list-item__deleted-text").text
                        comment = comment + str(del_comm_cnt)
                        del_comm_cnt += 1
                    if(comments.get(comment) == None):
                        comments[comment] = ""
                        # get sub comments
                        if "comment-list-item__replies" in html:
                            # item.find_element(By.CSS_SELECTOR, "div.comment-list-item__replies").click()
                            sub_comments = item.find_element(By.CSS_SELECTOR, "div.comment-list-item__replies")
                            actions.move_to_element(sub_comments).click(on_element=sub_comments).perform()

                            sub_com_html = item.find_element(By.CSS_SELECTOR, '//*/div/section/section[2]').get_attribute("innerHTML")
                            # sub_com_html = sub_com_html.get_attribute("innerHTML")
                            # print(sub_com_html)
                            # if "load-next__replies" in html:
                            #     more_sub_comments = item.find_element(By.CSS_SELECTOR, "div.load-next__replies")
                            #     actions.move_to_element(more_sub_comments).click(on_element=more_sub_comments).perform()

                except:
                    pass

                # Click the box to access the sub-comments and Scrape the sub-comments for each comment
        except:
            pass
        miN = miN + 1500
    for i in comments:
        print(i)
        # Save the results to a csv file
