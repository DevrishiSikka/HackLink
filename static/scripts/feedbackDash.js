function openPopup() {
      // Code to open the popup
      document.getElementById('popup').style.display = 'block';
    }

    function closePopup() {
      // Code to close the popup
      document.getElementById('popup').style.display = 'none';
    }

    function submitForm() {
      // Get form data
      var formName = document.getElementById('formName').value;
      var formDescription = document.getElementById('formDescription').value;

      // Perform Ajax request to submit the form data to Flask
      fetch('feedback/form/create', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            formName: formName,
            formDescription: formDescription,
          }),
        })
        .then(response => response.json())
        .then(data => {
          // Access the generated UUID from the response
          const uuid = data.uuid;

          // Redirect to another URL with the UUID as a query parameter
          window.location.href = `feedback/form/new?uuid=${uuid}`;
        })
        .catch(error => {
          console.error('Error:', error);
        });
    }

    document.querySelector('.create_form').addEventListener('click', openPopup);

    document.getElementById('close').addEventListener('click', function(event) {
      // Prevent the default form submission behavior
      event.preventDefault();

      // Call the submitForm function when the submit button is clicked

      // Close the popup
      closePopup();
    });
    document.getElementById('submit').addEventListener('click', function(event) {
      // Prevent the default form submission behavior
      event.preventDefault();

      // Call the submitForm function when the submit button is clicked
      submitForm();
    });

    