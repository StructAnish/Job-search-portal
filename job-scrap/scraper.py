from flask import Flask, request, render_template, jsonify, url_for
from flask_socketio import SocketIO, emit
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Mulithreading:
import time

app = Flask(__name__)
socketio = SocketIO(app)

options = webdriver.ChromeOptions()

options.add_argument('--headless=new') # Run Chrome without its UI
options.add_argument('--disable-gpu')
options.add_argument("--disable-images")
options.add_argument("--incognito")
# options.add_argument("--no-sandbox")  # Bypass OS security model
# options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
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

@app.route("/saved_jobs")
def saved_jobs():
    return render_template("/jobs/saved_jobs.html")

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

@app.route("/about")
def about():
    return render_template("/social/about.html")


indeedStatus = glassdoorStatus = 1

#.................... Scraping API code .........................
@socketio.on('job_search')  # Listen for 'job_search' event from client
def handle_job_search(data):
    domain = data["jobTitle"]
    location = data["location"]

    time1 = time.time()

    scrapeJobs(domain, 'https://in.indeed.com/', "text-input-what", location, "text-input-where",
                "job_seen_beacon", "jobTitle", "jcs-JobTitle", "css-1p0sjhy", "css-92r8pb",
                "css-9446fg", "css-qvloho", "salary-snippet-container")
    
    scrapeJobs(domain, 'https://www.glassdoor.co.in/Job/index.htm', "searchBar-jobTitle", location,"searchBar-location",
                "jobCard", "JobCard_jobTitle___7I6y", "JobCard_jobTitle___7I6y",
                 "JobCard_location__rCz3x", "EmployerProfile_compactEmployerName__LE242",
                 "JobCard_jobDescriptionSnippet__yWW8q", "JobCard_listingAge__Ny_nG", "JobCard_salaryEstimate__arV5J")
    
    
    # This will tell no jobs are available
    if indeedStatus == 0 and glassdoorStatus == 0:
        emit("no_jobs", {})

    print("Time taken: ",time.time() - time1)


def scrapeJobs(domain, website, searchbarTag, location, locationSearchbarTag, cardTag, jobtitleTag, 
               joblinkTag, locationTag, companyTag, descriptionTag, jobPostedTag, salaryTag):
    
    global indeedStatus, glassdoorStatus

    driver = webdriver.Chrome(options = options)

    driver.get(website)
    time.sleep(0.8)

    locationSearchBar = driver.find_element(By.ID, locationSearchbarTag)
    locationSearchBar.clear()
    locationSearchBar.send_keys(location)

    searchBar = driver.find_element(By.ID, searchbarTag)
    searchBar.clear()
    searchBar.send_keys(domain)
    searchBar.send_keys(Keys.RETURN)
    time.sleep(1)

    results = driver.find_elements(By.CLASS_NAME, cardTag)

    # Checking if data is available or not
    if len(results):
        indeedStatus = glassdoorStatus = 1


        for result in results:
            job_title = result.find_element(By.CLASS_NAME, jobtitleTag).text
            job_link = result.find_element(By.CLASS_NAME, joblinkTag).get_attribute("href")
            job_location = result.find_element(By.CLASS_NAME, locationTag).text
            company_name = result.find_element(By.CLASS_NAME, companyTag).text
            description = result.find_element(By.CLASS_NAME, descriptionTag).text
            job_posted = result.find_element(By.CLASS_NAME, jobPostedTag).text

            try:
                job_salary = result.find_element(By.CLASS_NAME, salaryTag)
                job_salary = job_salary.text

            except:
                job_salary = ""
            
            emit("job_results",
                 {
                    "name" : company_name,
                    "title" : job_title,
                    "location": job_location,
                    "link" : job_link,
                    "description": description,
                    "posted" : job_posted,
                    "salary" : job_salary
                })
        
        driver.quit()
    
    else:
        if website == "https://in.indeed.com/":
            indeedStatus = 0
        else:
            glassdoorStatus = 0
    
    

if __name__ == '__main__':
    socketio.run(app, debug=True)
    # app.run(debug=True)
