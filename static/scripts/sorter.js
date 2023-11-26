document.addEventListener("DOMContentLoaded", function () {
  const participants = document.querySelectorAll(".participant-tables tbody tr");
  const filterButtons = {
    sortDayScholar: document.getElementById("sortDayScholar"),
    sortHosteller: document.getElementById("sortHosteller"),
    filterMale: document.getElementById("filterMale"),
    filterFemale: document.getElementById("filterFemale"),
  };

  const searchInput = document.getElementById("searchInput");
  searchInput.addEventListener("input", function () {
    searchParticipantTeamname("Name", searchInput.value.toLowerCase());
  });

  
  // Add event listeners to filter buttons
  filterButtons.sortDayScholar.addEventListener("click", function () {
    filterParticipants("Accomodation", "Dayscholar");
  });

  filterButtons.sortHosteller.addEventListener("click", function () {
    filterParticipants("Accomodation", "Hostel");
  });

  filterButtons.filterMale.addEventListener("click", function () {
    filterParticipants("Gender", "Male");
  });

  filterButtons.filterFemale.addEventListener("click", function () {
    filterParticipants("Gender", "Female");
  });

    function searchParticipantTeamname(criteria, value) {
    participants.forEach(participant => {
      const name = participant.querySelector("td:nth-child(1)").textContent.toLowerCase();
      const username = participant.querySelector("td:nth-child(2)").textContent.toLowerCase();
      const matches = name.includes(value) || username.includes(value);
      participant.style.display = matches ? "table-row" : "none";
    });
  }


  // Function to filter participants based on a given criteria
  function filterParticipants(criteria, value) {
    participants.forEach(participant => {
      const cell = participant.querySelector(`td:nth-child(${getColumnIndex(criteria)})`);
      participant.style.display = cell.textContent === value ? "table-row" : "none";
    });
  }

  // Function to get the column index based on the header text
  function getColumnIndex(headerText) {
    const headers = document.querySelectorAll(".participant-tables th");
    for (let i = 0; i < headers.length; i++) {
      if (headers[i].textContent.trim() === headerText) {
        return i + 1; // Adding 1 because nth-child is 1-indexed
      }
    }
    return -1; // Return -1 if header not found
  }

});



document.addEventListener("DOMContentLoaded", function() {
    // Get the close button and participant info container elements
    var closeButton = document.getElementById('close-btn');
    var participantInfoContainer = document.getElementById('participant-info-container');
    var container = document.querySelector('.container');

    // Add click event listener to the close button
    closeButton.addEventListener('click', function() {
        // Reset the background blur
        container.style.filter = 'none';

        // Hide the participant info container
        participantInfoContainer.style.display = 'none';
    });

    // Get all anchor tags with class "tooltip-container"
    var tooltipLinks = document.querySelectorAll('.tooltip-container');

    // Add click event listener to each anchor tag
    tooltipLinks.forEach(function(link) {
        link.addEventListener("click", function(event) {
            event.preventDefault();

            // Get the href attribute of the clicked anchor tag
            var href = link.getAttribute('href');
            
            // Make an AJAX request to the href endpoint
            fetch(href)
                .then(response => response.json())
                .then(data => {
                    // Display the fetched data in the participant info container
                    var informationContainer = document.querySelector('.information');
                    informationContainer.innerHTML = '';

                    // Create a logical order for displaying data
                    var order = ['participant_name', 'register_number', 'team_name', 'mobile_number', 'accomodation', 'email_id', 'hostel_block', 'gender', 'checked_in', 'onboarding_email_sent'];

                    // Iterate through the ordered keys
                    order.forEach(function(key) {
                        var label = document.createElement('label');
                        label.textContent = key.replace(/_/g, ' ').replace(/\b\w/g, function (l) { return l.toUpperCase(); }) + ': ';
                        informationContainer.appendChild(label);

                        var inputField = document.createElement('input');
                        inputField.type = 'text';
                        inputField.id = key;
                        inputField.value = data[key];
                        inputField.disabled = true;
                        informationContainer.appendChild(inputField);
                    });

                    // Show the participant info container
                    participantInfoContainer.style.display = 'flex';

                    // Blur the background
                    container.style.filter = 'blur(5px)';
                })
                .catch(error => console.error('Error:', error));

            // Prevent the link from redirecting (default behavior)
            return false;
        });
    });
});
