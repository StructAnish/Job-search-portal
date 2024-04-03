from flask import Flask, request, render_template, jsonify, url_for
from flask_socketio import SocketIO, emit
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Mulithreading:
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app)

options = webdriver.ChromeOptions()

options.add_argument('--headless=new') # Run Chrome without its UI
options.add_argument("--no-sandbox")  # Bypass OS security model
options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
# Add a real User-Agent header
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36")


jobs_info = []
# lock = threading.Lock()

# ...............Routes.............................
@app.route('/')
def index():
    return render_template('home.html')

@app.route("/jobs")
def jobs():
    return render_template("/jobs/jobs.html")

@app.route("/details")
def details():
    return render_template("/social/detail.html")

@app.route("/settings")
def settings():
    return render_template("/social/setting.html")

@app.route("/signup")
def signup():
    return render_template("/sign/signup.html")

@app.route("/signout")
def signout():
    return render_template("/sign/signout.html")

# @app.route("/feedback")
# def feedback():
#     return render_template("")




#.................... Scraping API code .........................
@socketio.on('job_search')  # Listen for 'job_search' event from client
def handle_job_search(data):
    domain = data["jobTitle"]
    location = data["location"]

    time1 = time.time()

    scrapeJobs(domain, 'https://in.indeed.com/', "text-input-what", "resultContent", "jobTitle", "jcs-JobTitle", "css-1p0sjhy", "css-92r8pb")
    scrapeJobs(domain, 'https://www.glassdoor.co.in/Job/index.htm', "searchBar-jobTitle", "jobCard", "JobCard_jobTitle___7I6y", "JobCard_jobTitle___7I6y", "JobCard_location__rCz3x", "EmployerProfile_compactEmployerName__LE242")

    print("Time taken: ",time.time() - time1)


# def scrapeJobs(domain, website, searchbarTag, location, locationSearchbarTag ,cardTag, jobtitleTag, joblinkTag, locationTag, companyTag):
def scrapeJobs(domain, website, searchbarTag, cardTag, jobtitleTag, joblinkTag, locationTag, companyTag):

    driver = webdriver.Chrome(options = options)

    driver.get(website)
    time.sleep(0.5)

    # locationSearchBar = driver.find_element(By.ID, locationSearchbarTag)
    # locationSearchBar.clear()
    # locationSearchBar.send_keys(location)
    # locationSearchBar.send_keys(Keys.RETURN)

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
        
        emit("job_results", {"name" : company_name, "title" : job_title, "location": job_location, "link" : job_link})
    
    

if __name__ == '__main__':
    socketio.run(app, debug=True)
    # app.run(debug=True)
