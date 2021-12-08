from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep
import csv

URL = 'https://www.youtube.com/post/UgxFxRRLBG2CZVTkTtt4AaABCQ'
CSS_CLASS_ITEMS = 'ytd-item-section-renderer'

service = Service('./chromedriver')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

driver.get(URL)

sleep(3)

for _ in range(6):
    driver.execute_script('window.scrollTo(0, 100000);')
    sleep(2)

items = driver.find_elements_by_class_name(CSS_CLASS_ITEMS)
comments = driver.find_elements(By.XPATH, "//yt-formatted-string[@class='style-scope ytd-comment-renderer']")
comments = [c.text for c in comments if c.text]

count = 0

with open('data.csv', mode='w') as csv_file:
    writer = csv.writer(csv_file, delimiter=',', quotechar='"')
    writer.writerow(['username', 'n_weeks', 'comment', 'channel_url'])
    for item in items:
        anchor_tags = item.find_elements_by_tag_name('a')
        if not anchor_tags:
            continue
        aa = [a.text for a in anchor_tags if a.text]
        hrefs = [a.get_attribute('href') for a in anchor_tags if a.get_attribute('href')]
        hrefs = [href for href in hrefs if 'channel' in href]
        if not hrefs:
            continue
        channel_url = hrefs[0] # all of the first thing inside of hrefs, index 0
        if len(aa) in (3, 4):
            comment = comments[count].replace('\n', ' ')
            count += 1
            username, n_weeks, *_ = aa
            print(username, n_weeks, channel_url)
            writer.writerow([username, n_weeks, comment, channel_url])

driver.close()
