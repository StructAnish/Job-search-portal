const button = document.querySelector("button");

// Getting the domain when button gets clicked
button.addEventListener("click", async function() {
    const domain = this.innerText;
    const response = await fetch('/get-domain', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        // passing the domain for python to fetch
        body: JSON.stringify({ domain: domain })
    })

    // Fetching back the jobs list from python
    const data = await response.json();
    console.log(data)

    // If button is pressed 2 times, it is appending the results. To solve this,  create a parent div and at the starting set its innerHtml to ""
    jobsSection = document.getElementById("jobsSection");
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


    });
    

});