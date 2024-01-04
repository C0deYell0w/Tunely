document.addEventListener("DOMContentLoaded", function() {
    // Get the search icon element
    var searchIcon = document.querySelector(".left-navbar-search-icon");

    // Get the search tab element
    var searchTab = document.querySelector(".search-tab");

    // Add a click event listener to the search icon
    searchIcon.addEventListener("click", function() {
        // Toggle the display property of the search tab
        if (searchTab.style.display === "none" || searchTab.style.display === "") {
            searchTab.style.display = "block";
            searchInput.focus();
        } else {
            searchTab.style.display = "none";         
        }
    });
});

const searchInput = document.getElementById('search-input');
const clearIcon = document.getElementById('clear-icon');

// Add an event listener to the search input
searchInput.addEventListener('input', function() {
    if (searchInput.value.length > 0) {
        clearIcon.style.display = 'block'; // Show clear icon when text is typed
    } else {
        clearIcon.style.display = 'none'; // Hide clear icon when text is cleared
    }
});

// Add an event listener to the clear icon
clearIcon.addEventListener('click', function() {
    searchInput.value = ''; // Clear the text
    clearIcon.style.display = 'none'; // Hide the clear icon
    searchInput.focus();
});


    document.addEventListener("DOMContentLoaded", function () {
        // Get references to elements
        const sidePanel = document.getElementById("sidePanel");
        const topNavbar = document.querySelector(".top-navbar");
        const bodyContainer = document.querySelector(".body-container");
        const searchTab = document.querySelector(".search-tab");
        const searchInput = searchTab.querySelector("input");
        const clearIcon = document.querySelector("#clear-icon");
        const sidePanelIcon = document.querySelector(".sidepanel-icon");
        const bannerContainer = document.querySelector(".banner-img-container");


        
        // Initialize the side panel as hidden
        let isSidePanelOpen = false;

        // Function to toggle the side panel and adjust widths
        function toggleSidePanel() {
            isSidePanelOpen = !isSidePanelOpen;

            if (isSidePanelOpen) {
                // Show the side panel
                sidePanel.style.right = ".3%";
                topNavbar.style.width = "70%";
                bodyContainer.style.width = "70%";
                searchTab.style.left = "27%";
                clearIcon.style.left ="14rem";
                searchInput.style.padding = "15px 2.5rem 15px 2rem";
                bannerContainer.style.width = "69.1%"

            } else {
                // Hide the side panel
                sidePanel.style.right = "-23%";
                topNavbar.style.width = "93%";
                bodyContainer.style.width = "93%";
                searchTab.style.left = "20%";
                clearIcon.style.left = "17.6rem";
                searchInput.style.padding = "15px 2rem 15px 2rem";
                bannerContainer.style.width = "92.1%"
            }
        }

        // Add a click event listener to the side panel icon
        sidePanelIcon.addEventListener("click", toggleSidePanel);
    });


    const volumeUpIcon = document.getElementById("volume-up-icon");
    const volumeSliderToggle = document.getElementById("slider-toggle");

    volumeUpIcon.addEventListener("click", function() {
    if (volumeSliderToggle.style.display === "block") {
        volumeSliderToggle.style.display = "none";
    } else {
        volumeSliderToggle.style.display = "block";
    }
    });
    


   