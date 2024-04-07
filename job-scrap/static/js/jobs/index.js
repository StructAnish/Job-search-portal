const searchInputs = document.querySelectorAll('.search-input');
const closeButtons = document.querySelectorAll('.close');
const searchFields = document.querySelectorAll('.search-field');


searchInputs.forEach((searchInput, index) => {
    // Input event listener
    searchInput.addEventListener('input', () => {
        if (searchInput.value.length > 0) {
            closeButtons[index].classList.remove('close-hidden');
        } else {
            closeButtons[index].classList.add('close-hidden');
        }
    });

    // Which element is at focus not
    searchInput.addEventListener('focus', () => {
        searchFields[index].classList.add('focus');
    });
    searchInput.addEventListener('blur', () => {
        searchFields[index].classList.remove('focus');
    });
});

// Close button css
closeButtons.forEach((closeButton, index) => {
    closeButton.addEventListener('click', () => {
        searchInputs[index].value = "";
        closeButton.classList.add('close-hidden');
    });
});
