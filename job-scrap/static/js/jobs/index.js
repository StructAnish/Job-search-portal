document.getElementById("searchForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent default form submission

    const jobTitle = document.getElementById("title").value;
    const location = document.getElementById("location").value;

    // console.log(jobTitle);

    // Send data to server-side script using Fetch API
    // Change this link to the link where the python code will run after deployment
    fetch("/api/jobs", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ jobTitle, location })
    })
    .then(response => response.json())
    .then(data => {
      // Display scraped results on the webpage
      displayScrapedJobs(data);
    })
    .catch(error => {
      console.error("Error sending data:", error);
    });
  });

  function displayScrapedJobs(data) {
    const jobsSection = document.getElementById("job-results");
    jobsSection.innerHTML = ""

    data.forEach(jobData => {

        const anchor = document.createElement('a');
        anchor.href = jobData.link;

        const heading = document.createElement('h2')
        heading.innerText = jobData.title;
        anchor.appendChild(heading);

        const location = document.createElement('p');
        location.innerText = jobData.name + "\n" + jobData.location;

        jobsSection.appendChild(anchor);
        jobsSection.appendChild(location);
    })
  };