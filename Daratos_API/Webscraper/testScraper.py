import selenium, time, os
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class WebDriver(webdriver.Chrome):
    def __init__(self, headless):
        options = Options()
        if (headless == False):
            options.add_argument("--start-maximized")
        else:
            options.headless = headless
        self.driver = webdriver.Chrome(r'chromedriver.exe', chrome_options=options)
        self.driver.implicitly_wait(1)

    def quit(self):
        self.driver.quit()
        print ("Driver exited successfully.\n")

    def loadWebsite(self, url):
        try:
            self.driver.get(url)
        except Exception as e:
            self.quit()
            print("Error loading website {}.. \n".format(url) + str(e))

    def getTitle(self):
        try:
            return self.driver.title
        except Exception as e:
            self.quit()
            return "Unable to extract title from news article. \n {}".format(str(e))

    def getAuthor(self):
        try:
            author = self.driver.find_element_by_xpath("//div[contains(text(), 'By')]").text
            author = author.replace('By ', '')
            return author
        except Exception as e:
            return "Error in getting author... \n" + str(e)

    def getBody(self):
        try:
            bodyText = ""
            itemList = self.driver.find_elements_by_xpath('//div/p')
            for item in itemList:
                bodyText += item.text + '\n'
            return bodyText
        except Exception as e:
            bodyText += "Error in grabbing body text.. \n" + str(e)
            return bodyText


headless = True
url = "https://www.nbcnews.com/politics/donald-trump/pompeo-admits-he-was-controversial-call-between-trump-ukrainian-president-n1061101"
url = input("Please enter an NBC article URL: ")

wd = WebDriver(headless)
wd.loadWebsite(url)

titleText = wd.getTitle()
bodyText = wd.getBody()
authorText = wd.getAuthor()
wd.quit()

open('log.txt', 'w').close()
article = {"Title": titleText, "Author": authorText, "Body": bodyText}
print(article,  file=open('log.txt', 'w'))
