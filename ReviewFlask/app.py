

from flask import Flask, render_template, request
from flask_cors import cross_origin
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import pandas as pd
import numpy as np
from selenium import webdriver
import time

app = Flask(__name__)

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/review',methods=['POST','GET']) # route to show the review comments in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            searchString = request.form['content'].replace(" ","")
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString
            uClient = uReq(flipkart_url)
            flipkartPage = uClient.read()
            uClient.close()
            flipkart_html = bs(flipkartPage, "html.parser")
            bigboxes = flipkart_html.findAll("div", {"class": "_1AtVbE col-12-12"})
            del bigboxes[0:3]
            box = bigboxes[0]
            productLink = "https://www.flipkart.com" + box.div.div.div.a['href']
            print("Product Link: " + productLink)
            filename = searchString + ".csv"
            fw = open(filename, "w")
            headers = "Customer Name, Rating, Heading, Comment \n"
            fw.write(headers)
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
            #driver = webdriver.Chrome()
            driver.get(productLink)
            time.sleep(7)
            driver.find_element_by_xpath("//div[@class='col JOpGWq']/a").click()


            time.sleep(7)
            print("It Works")

            Name = []
            Rating = []
            Heading = []
            Result = []

            Count = 0
            while driver.find_element_by_class_name("_1LKTO3"):
                Count += 1
                if (Count >= 10):
                    break

                Review_Elements = driver.find_elements_by_xpath(
                    "//div[@class='_1AtVbE col-12-12']/div/div/div[@class='col _2wzgFH K0kLPL']")
                for review in Review_Elements:
                    for review1 in review.find_elements_by_xpath(
                            "//div[@class='row _3n8db9']/div/p[@class='_2sc7ZR _2V5EHH']"):
                        try:
                            name = review1.text
                        except:
                            name = 'No Name'
                        Name.append(name)
                    for review2 in review.find_elements_by_xpath("//div[@class='_3LWZlK _1BLPMq']"):
                        try:
                            rating = review2.text
                        except:
                            rating = "No Rating"
                        Rating.append(rating)
                    for review3 in review.find_elements_by_xpath(
                            "//div[@class='col _2wzgFH K0kLPL']/div/p[@class='_2-N8zT']"):
                        try:
                            heading = review3.text
                        except:
                            heading = "No Heading"
                        Heading.append(heading)
                    for review4 in review.find_elements_by_xpath("//div[@class='t-ZTKy']"):
                        try:
                            result = review4.text
                        except:
                            result = "No Result"
                        Result.append(result)
                    break
                driver.find_elements_by_class_name("_1LKTO3")[-1].click()
                time.sleep(7)
            AllInfo = pd.DataFrame(np.column_stack([Name, Rating, Heading, Result]),
                                   columns=["Name", "Rating", "Heading", "Result"])

            return render_template('results.html', reviews=AllInfo[0:(len(AllInfo)-1)])
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
    # return render_template('results.html')

    else:
        return render_template('index.html')

if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
	app.run(debug=True)
