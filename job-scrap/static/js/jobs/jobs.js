import {firebaseConfig} from '../sign/config.js';
firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();
const db = firebase.firestore();

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

    <div class='about_company'>
      <div class='company_name'>Company: ${data.name}</div>
      <div class='company_location'>Location: ${data.location}</div>
      <div class='salary'>${data.salary}</div>
      <div class='description'>Description: ${data.description}</div>
      <div class='posted'>${data.posted}</div>
    </div>
    `;

  job.appendChild(jobLink);
  
  const saveButton = document.createElement('button');
  saveButton.className = "save-button";
  saveButton.setAttribute("title", "save");
  job.appendChild(saveButton);
  saveButton.innerHTML = "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 384 512'><path d='M0 48C0 21.5 21.5 0 48 0l0 48V441.4l130.1-92.9c8.3-6 19.6-6 27.9 0L336 441.4V48H48V0H336c26.5 0 48 21.5 48 48V488c0 9-5 17.2-13 21.3s-17.6 3.4-24.9-1.8L192 397.5 37.9 507.5c-7.3 5.2-16.9 5.9-24.9 1.8S0 497 0 488V48z'/></svg>"
  jobsSection.appendChild(job);
  
  saveButton.addEventListener("click", () => {
    console.log("I was clicked");
      // // If user is logged in
      auth.onAuthStateChanged(user => {
        if (user){
          console.log('user logged in', user)
          saveButton.innerHTML = ' <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"><path fill="#31acff" d="M0 48V487.7C0 501.1 10.9 512 24.3 512c5 0 9.9-1.5 14-4.4L192 400 345.7 507.6c4.1 2.9 9 4.4 14 4.4c13.4 0 24.3-10.9 24.3-24.3V48c0-26.5-21.5-48-48-48H48C21.5 0 0 21.5 0 48z"/></svg> '
          saveButton.disabled = true;

          // Adding data to database
          db.collection('jobs').add({
            // job: `${jobs[index]}`
            title: data.title,
            name: data.name,
            link: data.link,
            location: data.location,
            salary: data.salary,
            description: data.description,
            posted: data.posted,
            
          }).then(() => {
            // Do something after document has been added
          })

        } else {
          console.log('User logged out')
        }
  })
  });

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