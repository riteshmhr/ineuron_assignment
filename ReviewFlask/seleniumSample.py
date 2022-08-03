import pandas as pd
import numpy as np
from selenium import webdriver
import time


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--incognito')
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument('-disk-cache-size-300000000000')
driver = webdriver.Chrome(options=chrome_options)

driver.get(r'https://www.flipkart.com/apple-iphone-7-black-32-gb/product-reviews/itmen6daftcqwzeg?pid=MOBEMK62PN2HU7EE&lid=LSTMOBEMK62PN2HU7EEINTGNU&marketplace=FLIPKART')
time.sleep(5)

Name = []
Rating = []
Heading = []
Result = []

Count =0
while driver.find_element_by_class_name("_1LKTO3"):
    Count+=1
    if(Count >= 5):
        break
    Review_Elements = driver.find_elements_by_xpath("//div[@class='_1AtVbE col-12-12']/div/div/div[@class='col _2wzgFH K0kLPL']")
    for review in Review_Elements:
        for review1 in review.find_elements_by_xpath("//div[@class='row _3n8db9']/div/p[@class='_2sc7ZR _2V5EHH']"):
            name = review1.text
            Name.append(name)
        for review2 in review.find_elements_by_xpath("//div[@class='_3LWZlK _1BLPMq']"):
            rating = review2.text
            Rating.append(rating)
        for review3 in review.find_elements_by_xpath("//div[@class='col _2wzgFH K0kLPL']/div/p[@class='_2-N8zT']"):
            heading = review3.text
            Heading.append(heading)
        for review4 in review.find_elements_by_xpath("//div[@class='t-ZTKy']"):
            result = review4.text
            Result.append(result)
        break
    driver.find_elements_by_class_name("_1LKTO3")[-1].click()
    time.sleep(6)

#Putting all data in PD Data Frame
AllInfo = pd.DataFrame(np.column_stack([Name, Rating, Heading, Result]), columns=["Name","Rating","Heading","Result"])
print(AllInfo)


