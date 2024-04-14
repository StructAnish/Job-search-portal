import {firebaseConfig} from '../sign/config.js';
firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();
const db = firebase.firestore();

// If user is logged in
auth.onAuthStateChanged(user => {
    if (user){
        console.log('user logged in', user)
    }
    else{
        console.log('user logged Out', user)
        
    }
});

// Gettings from database and displaying it
db.collection('jobs').get().then(snapshot => {
    const data = snapshot.docs;
    data.forEach(doc => {
        // console.log(doc.data())
        
        // Displaying fetched data from firestore
        const fetched_data = doc.data()
        const jobResults = document.getElementById("job-results");
        const job = document.createElement('div');
        job.className = "job";
        job.id = doc.id;

        const jobLink = document.createElement('a');
        jobLink.className = "job-link";
        jobLink.setAttribute("href", fetched_data['link']);
        jobLink.setAttribute("target", "_blank");

        
        jobLink.innerHTML = `
        <h2 class='jobTitle'>${fetched_data['title']}</h2>

        <div class='about_company'>
            <div class='company_name'>${fetched_data['name']}</div>
            <div class='company_location'>${fetched_data['location']}</div>
            <div class='salary'>${fetched_data['salary']}</div>
            <div class='description'>${fetched_data['description']}</div>
            <div class='posted'>${fetched_data['posted']}</div>
        </div>

        `;

        job.appendChild(jobLink);
        
        const save = document.createElement('button');
        save.className = "save-button";
        job.appendChild(save);
        save.innerHTML = ' <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"><path fill="#31acff" d="M0 48V487.7C0 501.1 10.9 512 24.3 512c5 0 9.9-1.5 14-4.4L192 400 345.7 507.6c4.1 2.9 9 4.4 14 4.4c13.4 0 24.3-10.9 24.3-24.3V48c0-26.5-21.5-48-48-48H48C21.5 0 0 21.5 0 48z"/></svg> '

        jobResults.appendChild(job);

    })

    

    // Deleting the data from database
    const jobs = document.querySelectorAll('.job');
    const saveButtons = document.querySelectorAll('.save-button');

    saveButtons.forEach((saveButton, index) => {
        saveButton.addEventListener("click", () => {
            
            saveButton.innerHTML = " <svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 384 512'><path d='M0 48C0 21.5 21.5 0 48 0l0 48V441.4l130.1-92.9c8.3-6 19.6-6 27.9 0L336 441.4V48H48V0H336c26.5 0 48 21.5 48 48V488c0 9-5 17.2-13 21.3s-17.6 3.4-24.9-1.8L192 397.5 37.9 507.5c-7.3 5.2-16.9 5.9-24.9 1.8S0 497 0 488V48z'/></svg> ";

            db.collection("jobs").doc(jobs[index].id).delete()
            .then(() => {
                console.log("Document successfully deleted!");

                // new Promise((resolve) => setTimeout(resolve, 5));
                // jobs[index].style.display = "none";

                }).catch((error) => {
                    console.error("Error removing document: ", error);
            });           
            
            // Add transitions here for deleting            
            jobs[index].style.display = "none";

        })
    });

});

