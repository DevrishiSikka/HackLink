# HackLink Hackathon Management System

## Introduction

This Flask-based web application is designed for managing participant registrations for an event. The application provides functionality for adding individual participants manually, uploading participant information via Excel files, and scanning participant QR codes for check-ins.

## Features

1. **Participant Registration:**
   - Participants can be added individually through a user-friendly form.
   - Validation ensures that duplicate entries with the same register number are not allowed.

2. **Excel Upload:**
   - Bulk participant data can be uploaded using an Excel file.
   - The system checks for existing participants and adds new ones accordingly.
   - Asynchronous processing is implemented using Celery to handle large data uploads without affecting the application's responsiveness.

3. **QR Code Generation:**
   - A QR code is generated for each participant upon registration.
   - The QR code is saved as an image in the 'qrcodes' folder.

4. **Email Notification:**
   - After successful registration, participants receive an email with their details and a QR code attachment.
   - Email functionality is integrated using the Mailgun API.

5. **Dashboard:**
   - The dashboard provides an overview of participant statistics, including counts based on gender, accommodation type, and check-ins.

6. **Check-In System:**
   - Participants can be checked in by scanning their QR codes.
   - The system updates the participant's check-in status in the database.

## Setup Instructions

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/flask-registration-system.git
   cd flask-registration-system
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Credentials:**
   - Create a `config.ini` file and provide the necessary credentials, including the Mailgun API key and other configuration details.

4. **Start Celery Worker:**
   ```bash
   celery -A app.celery worker --loglevel=info
   ```
   This command starts a Celery worker that will process background tasks.

5. **Start Flower for Monitoring:**
   ```bash
   celery -A app.celery flower
   ```
   The Flower web-based monitoring tool can be accessed at `http://localhost:5555` by default. It provides insights into task execution and worker status.

   **Note:** Ensure that you have Redis running, as Celery uses it as a message broker.

6. **Run the Application:**
   ```bash
   python app.py
   ```
   Access the application by navigating to `http://localhost:5000` in your web browser.

## Dependencies

The Flask Registration System relies on the following third-party libraries and services:

- **Flask:** A lightweight WSGI web application framework in Python.
  - [Flask Documentation](https://flask.palletsprojects.com/en/2.1.x/)

- **SQLAlchemy:** SQL toolkit and Object-Relational Mapping (ORM) for Python.
  - [SQLAlchemy Documentation](https://docs.sqlalchemy.org/en/20/)

- **Celery:** Distributed task queue for background processing.
  - [Celery Documentation](https://docs.celeryproject.org/en/stable/)

- **pandas:** Data manipulation and analysis library.
  - [pandas Documentation](https://pandas.pydata.org/pandas-docs/stable/)

- **requests:** HTTP library for sending requests.
  - [requests Documentation](https://docs.python-requests.org/en/latest/)

- **qrcode:** QR code generation library.
  - [qrcode Documentation](https://pypi.org/project/qrcode/)

- **Flask-SocketIO:** WebSocket support for Flask applications.
  - [Flask-SocketIO Documentation](https://flask-socketio.readthedocs.io/en/latest/)

- **Flask-WTF:** Simple integration of Flask and WTForms.
  - [Flask-WTF Documentation](https://flask-wtf.readthedocs.io/en/stable/)

- **Werkzeug:** A WSGI utility library for Python.
  - [Werkzeug Documentation](https://werkzeug.palletsprojects.com/en/3.1.x/)

- **Celery Flower:** Real-time web-based monitoring tool for Celery.
  - [Celery Flower Documentation](https://flower.readthedocs.io/en/latest/)

- **Mailgun:** Email service for sending registration confirmation emails.
  - [Mailgun Documentation](https://www.mailgun.com/)

**Note:** Ensure to sign up and configure your own credentials for services like Mailgun before running the application.

**Additional Setup Steps:**
- Create accounts and obtain API keys for third-party services like Mailgun.
- Configure the necessary credentials in the `config.ini` file.

**Important:** Make sure to comply with the terms of use and licensing agreements for each third-party service.



## Additional Notes

- Make sure to have Redis installed and running for Celery to work properly.

## Contributors

- Devrishi Sikka

Feel free to contribute to the project by submitting issues or pull requests!

