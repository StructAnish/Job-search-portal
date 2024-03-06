from flask import Flask, request, render_template, jsonify
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import threading    # Mulithreading
import time

app = Flask(__name__)

# Configure Selenium
options = webdriver.ChromeOptions()
# If you want to hide chrome tabs, uncomment the following line
# options.add_argument('--headless')  # Run Chrome in headless mode

# Global variable for storing job infos from different sites:
jobs_info = []


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-domain', methods=['POST'])
def get_domain():
    global jobs_info
    domain = request.json.get('domain')

    time1 = time.time()

    # Multitasking using multithreading
    # Scraping indeed
    t1 = threading.Thread(target = scrapeJobs, args = (domain, 'https://in.indeed.com/', "text-input-what", "resultContent", "jobTitle", "jcs-JobTitle", "css-1p0sjhy", "css-92r8pb"))
    
    # Scraping glassdoor
    t2 = threading.Thread(target = scrapeJobs, args = (domain, 'https://www.glassdoor.co.in/Job/index.htm', "searchBar-jobTitle", "jobCard", "JobCard_jobTitle___7I6y", "JobCard_jobTitle___7I6y", "JobCard_location__rCz3x", "EmployerProfile_employerName__qujuA"))
    
    # Start thread
    t1.start()
    t2.start()
    # End thread execution
    t1.join()
    t2.join()

    time2 = time.time()
    print("Time taken: ",time2 - time1)
    # Existing Scraping LinkedIn code here: ..

    # ............................................................................

    return jobs_info
    


# Function for scraping individual site
def scrapeJobs(domain, website, searchbarTag, cardTag, jobtitleTag, joblinkTag, locationTag, companyTag):
    global jobs_info
    
    driver = webdriver.Chrome(options = options)
    driver.get(website)
    time.sleep(0.5)

    searchBar = driver.find_element(By.ID, searchbarTag)
    searchBar.clear()
    searchBar.send_keys(domain)
    searchBar.send_keys(Keys.RETURN)

    results = driver.find_elements(By.CLASS_NAME, cardTag)

    for result in results:
        job_title = result.find_element(By.CLASS_NAME, jobtitleTag).text
        job_link = result.find_element(By.CLASS_NAME, joblinkTag).get_attribute("href")
        job_location = result.find_element(By.CLASS_NAME, locationTag).text
        company_name = result.find_element(By.CLASS_NAME, companyTag).text 
        
        # Appending to global list
        jobs_info.append({"name" : company_name, "title" : job_title, "location": job_location, "link" : job_link})
    
    driver.quit()
    return




if __name__ == '__main__':
    app.run(debug=True)
