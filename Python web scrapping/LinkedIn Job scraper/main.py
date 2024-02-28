from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException , ElementClickInterceptedException 
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
import json

class auto_bot:

    def __init__(self, data):

                self.email = data['email']
                self.password = data['password']
                self.keywords = data['keywords']
                self.location = data['location']
                options = webdriver.ChromeOptions()
                options.add_experimental_option("detach", True)
                self.driver = webdriver.Chrome(options=options)

    def login_linkedin(self):

        self.driver.get("https://www.linkedin.com/login")

        login_email = self.driver.find_element("name",'session_key')
        login_email.clear()
        login_email.send_keys(self.email)
        login_pass = self.driver.find_element("name",'session_password')
        login_pass.clear()
        login_pass.send_keys(self.password)
        login_pass.send_keys(Keys.RETURN)
 
    def job_search(self):
        

        # go to Jobs
        jobs_link = self.driver.find_element(By.LINK_TEXT,'Jobs')
        jobs_link.click()
        time.sleep(3)

        # search based on keywords and location and hit enter
        search_keywords = self.driver.find_element(By.CSS_SELECTOR,".jobs-search-box__text-input[aria-label='Search by title, skill, or company']")
        search_keywords.clear()
        search_keywords.send_keys(self.keywords)
        time.sleep(2)
        search_location = self.driver.find_element(By.CSS_SELECTOR, ".jobs-search-box__text-input[aria-label='City, state, or zip code']")
        search_location.clear()
        search_location.send_keys(self.location)
        search_keywords.send_keys(Keys.ENTER)


if __name__ == '__main__':

        with open('configure.json') as config_file:
            data = json.load(config_file)

            bot = auto_bot(data)
            bot.login_linkedin()
            time.sleep(3)
            bot.job_search()
