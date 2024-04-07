const socket = io();

const loader = document.querySelector(".loader");
const jobsSection = document.getElementById("job-results");

// Function for displaying jobs
function displayScrapedJobs(data) {

  const job = document.createElement('div');
  job.className = "job";

  const jobLink = document.createElement('a');
  jobLink.className = "job-link";
  jobLink.setAttribute("href", data.link);
  jobLink.setAttribute("target", "_blank");
  
  jobLink.innerHTML = `
    <h2 class='jobTitle'>${data.title}</h2>
    <div class='company_location'>
      <span class='company_name'>Company: ${data.name}</span>
      <span class='company_location'>Location: ${data.location}</span>
      <span class='salary'>${data.salary}</span>
      <span class='description'>Description: ${data.description}</span>
      <span class='posted'>${data.posted}</span>
    </div>
    `;

  job.appendChild(jobLink);
  jobsSection.appendChild(job);
};


// Submit button event handler function
document.getElementById("searchForm").addEventListener("submit", function(event) {
  event.preventDefault(); // Prevent default form submission

  // remove loader-hidden class of loader
  loader.classList.remove("loader-hidden");

  jobsSection.innerHTML = "";

  const jobTitle = document.getElementById("title").value;
  const location = document.getElementById("location").value;

  // Emit data to server-side with SocketIO
  socket.emit('job_search', { jobTitle, location });
});


// Listen for 'job_results' event
socket.on('job_results', function(data) {
  // Hide loading screen
  if(loader.classList.contains("loader-hidden") == false){
    loader.classList.add("loader-hidden");
  }

  // Display scraped results on the webpage
  displayScrapedJobs(data);
});

// What to display when no jobs are available
socket.on('no_jobs', function(data) {
  if(loader.classList.contains("loader-hidden") == false){
    loader.classList.add("loader-hidden");
  }

  jobsSection.innerHTML = `
      <h1>The search did not match any jobs.</h1>
      <h2>Search suggestions:</h2>
      <ul>
      <li>Try more general keywords</li>
      <li>Check your spelling</li>
      <li>Replace abbreviations with the entire word</li>
      </ul>
      `;
});