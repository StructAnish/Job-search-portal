from flask import Flask, request, render_template, jsonify
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

app = Flask(__name__)

# Configure Selenium
options = webdriver.ChromeOptions()
# If you want to hide chrome tabs, uncomment the following line
# options.add_argument('--headless')  # Run Chrome in headless mode
driver = webdriver.Chrome(options=options)

# Global variable for storing job infos from different sites:
jobs_info = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-domain', methods=['POST'])
def get_domain():
    domain = request.json.get('domain')

    # .......... Mention sites from which you want to scrape data.................
    # Scrape indeed
    scrapeJobs(domain, 'https://in.indeed.com/', "text-input-what", "resultContent", "jobTitle", "jcs-JobTitle", "css-1p0sjhy", "css-92r8pb")

    # Scrape Glassdoor
    scrapeJobs(domain, 'https://www.glassdoor.co.in/Job/index.htm', "searchBar-jobTitle", "jobCard", "JobCard_jobTitle___7I6y", "JobCard_jobTitle___7I6y", "JobCard_location__rCz3x", "EmployerProfile_employerName__qujuA")

    # Existing Scraping LinkedIn code here: ..

    # ............................................................................

    return jsonify(jobs_info)
    


# Function for scraping individual site
def scrapeJobs(domain, website, searchbarTag, cardTag, jobtitleTag, joblinkTag, locationTag, companyTag):
    driver.get(website)

    searchBar = driver.find_element(By.ID, searchbarTag)
    searchBar.clear()
    searchBar.send_keys(domain)
    searchBar.send_keys(Keys.RETURN)

    results = driver.find_elements(By.CLASS_NAME, cardTag)

    print("Data here:\n\n")
    for result in results:
        job_title = result.find_element(By.CLASS_NAME, jobtitleTag).text
        job_link = result.find_element(By.CLASS_NAME, joblinkTag).get_attribute("href")
        job_location = result.find_element(By.CLASS_NAME, locationTag).text
        company_name = result.find_element(By.CLASS_NAME, companyTag).text 
        
        # Appending to global list 
        jobs_info.append({"name" : company_name, "title" : job_title, "location": job_location, "link" : job_link})
    
    return




if __name__ == '__main__':
    app.run(debug=True)
