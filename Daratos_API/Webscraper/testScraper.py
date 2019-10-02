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


headless = False
url = "https://www.nbcnews.com/politics/donald-trump/pompeo-admits-he-was-controversial-call-between-trump-ukrainian-president-n1061101"

wd = WebDriver(headless)
wd.loadWebsite(url)