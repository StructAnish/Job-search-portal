const socket = io();

const jobsSection = document.getElementById("job-results");
document.getElementById("searchForm").addEventListener("submit", function(event) {
  event.preventDefault(); // Prevent default form submission
  jobsSection.innerHTML = "";

  const jobTitle = document.getElementById("title").value;
  const location = document.getElementById("location").value;

  // Emit data to server-side with SocketIO
  socket.emit('job_search', { jobTitle, location });
});

socket.on('job_results', function(data) {  // Listen for 'job_results' event
  // Display scraped results on the webpage
  displayScrapedJobs(data);
});

function displayScrapedJobs(data) {
  const jobsSection = document.getElementById("job-results");
  
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
      </div>
    `;

  job.appendChild(jobLink);
  jobsSection.appendChild(job);
};