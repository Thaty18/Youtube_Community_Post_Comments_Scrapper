from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep
import csv

CHANNEL_CLASS_NAME = 'ytd-grid-channel-renderer'

service = Service('./chromedriver')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

with open('data.csv', 'r') as f:
    reader = csv.reader(f, delimiter=',')
    next(reader)
    # count = 0

    with open('full_data.csv', 'w') as out:
        writer = csv.writer(out, delimiter=',', quotechar='"')

        writer.writerow(['username', 'n_weeks', 'comment', 'subscription_status', 'channel_url'])
        for username, n_weeks, comment, channel_url in reader:
            # count += 1
            # if count > 3:
            #     break
            channel_url += '/channels'
            driver.get(channel_url)
            sleep(2)
            subscription_status = 'N/A'
            channels = driver.find_elements(By.XPATH, "//span[@class='style-scope ytd-grid-channel-renderer']")
            # channels = driver.find_elements_by_class_name(CHANNEL_CLASS_NAME)
            if channels:
                for _ in range(20):
                    driver.execute_script('window.scrollTo(0, 100000);')
                    sleep(1)
                # channels = driver.find_elements_by_class_name(CHANNEL_CLASS_NAME)
                channels = driver.find_elements(By.XPATH, "//span[@class='style-scope ytd-grid-channel-renderer']")
                channels = [channel.text for channel in channels if channel.text]
                channels = [text.lower() for text in channels if 'subscribe' not in text.lower()]
                print(channels)
                if 'freecodecamp.org' in channels:
                    subscription_status = 'subscribed'
            print(username, n_weeks, channel_url, subscription_status)
            writer.writerow([username, n_weeks, comment, subscription_status, channel_url])

driver.close()