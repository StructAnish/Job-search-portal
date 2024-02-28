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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-domain', methods=['POST'])
def get_domain():
    domain = request.json.get('domain')
    
    # Replace this with your actual scraping logic using Selenium
    driver.get('https://in.indeed.com/')
    
    searchBar = driver.find_element(By.ID, "text-input-what")
    searchBar.clear()
    searchBar.send_keys(domain)
    searchBar.send_keys(Keys.RETURN)

    # Scrape
    results = driver.find_elements(By.CLASS_NAME, "resultContent")
    jobs_info = []

    for result in results:
        job_profile = result.find_element(By.TAG_NAME, "h2").text
        job_link = result.find_element(By.TAG_NAME, "a").get_attribute("href")
        job_name = result.find_element(By.CLASS_NAME, "css-92r8pb").text
        job_location = result.find_element(By.CLASS_NAME, "css-1p0sjhy").text
        
        jobs_info.append({"name" : job_name, "profile" : job_profile, "location": job_location, "link" : job_link})

    return jsonify(jobs_info)




if __name__ == '__main__':
    app.run(debug=True)
