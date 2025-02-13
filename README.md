# petzi-webhook

This is a Flask-based web application designed to store and display Petzi's webhook data.  
It allows users to view and manage information received via the webhook in a user-friendly interface.  
The application uses PostgreSQL for data storage and is containerized using Docker Compose for easy deployment and development.

## Features
- Webhook Integration: Capture and store data sent via webhooks.
- Data Visualization: View stored webhook data in a clean and organized manner.
- Pagination: Efficiently handle large datasets with paginated views.
- Dynamic Charts: Visualize data trends using interactive charts.
- User Authentication: Secure login system to protect access to the application.
- Password Management: Users can change their passwords securely.
- Rest API: Serves GET routes to retrieve the stored data.
- Dockerized: Easily deploy and run the application using Docker Compose.

## Technologies used
- Backend: Flask (Python)
- Database: PostgreSQL
- Frontend: HTML, CSS (Tabler CSS framework), JavaScript (ApexCharts for charts)
- Containerization: Docker, Docker Compose
- Authentication: Flask session management with password hashing using werkzeug.security
- Other Libraries: psycopg2 (PostgreSQL adapter for Python)

## Getting started
### 1. Clone the Repository

        git clone https://github.com/NoeBerdoz/petzi-webhook.git
        cd petzi-webhook

### 2. Set up
The current set up is not intended for production use, 
Please adapt the configurations if you mean to use it in a production environment, 
for security purposes.

To launch the backend and the database container use docker-compose.
At the root of the project, execute this command:
    
    docker-compose up --build

This will:
- Start a PostgreSQL database.
- Build and run the Flask application.
- Expose the application on http://127.0.0.1:5000/.

Open your browser and navigate to:
http://localhost:5000/auth/register

There create an account, and login, then you are good to go.

## API Endpoints
These routes can be use to add or retrieve data
from the server.

**POST `/insert`**
- **Description:** Entry point for the Petzi webhook, inserts ticket data.  
- **Response:** `{"message": "Data insert successfully"}` on success, otherwise `{"message": "Data insert failed"}`.

**GET `/chart/tickets/<int:event_id>`**
- **Description:** Returns ticket sales data formatted for an ApexCharts component.  
- **Response:** `{"categories": ["date1", "date2"], "sales": [count1, count2]}`.

**GET `/download_csv?event_id=<int:event_id>`**
- **Description:** Exports all tickets related to an event as a CSV file.  
- **Response:** CSV file download.

**GET `/buyers`**
- **Description:** Returns all buyers.  
- **Response:** JSON list of buyer records.

**GET `/locations`**
- **Description:** Returns all locations.  
- **Response:** JSON list of location records.

**GET `/events`**
- **Description:** Returns all events.  
- **Response:** JSON list of event records.

**GET `/tickets`**
- **Description:** Returns all tickets.  
- **Response:** JSON list of ticket records.

**GET `/sessions`**
- **Description:** Returns all sessions.  
- **Response:** JSON list of session records.

## Front-end routes
These routes can be use by a user, to navigate 
in the application.

**POST `/auth/login`**  
- **Description:** Authenticates a user and starts a session.  
- **Response:** Redirects to `/dashboard/home` on success, otherwise reloads login page with an error message.  

**GET `/auth/logout`**  
- **Description:** Logs out the user by clearing the session.  
- **Response:** Redirects to `/auth/login`.  

**POST `/auth/register`**  
- **Description:** Registers a new user with a hashed password.  
- **Response:** Redirects to `/auth/login` on success, otherwise reloads the registration page with an error message.  

**GET/POST `/auth/settings`**  
- **Description:** Allows logged-in users to change their password.  
- **Response:** Redirects to `/auth/settings` with a success or error message.  

**GET `/dashboard/home`**  
- **Description:** Displays the dashboard home page with event data.  
- **Response:** Renders `home.html` with a list of events.  

**GET `/dashboard/tickets`**  
- **Description:** Returns paginated ticket data and chart statistics.  
- **Response:** Renders `tickets.html` with ticket information and sales data.  

**GET `/dashboard/events`**  
- **Description:** Lists all events along with the number of tickets sold.  
- **Response:** Renders `events.html` with paginated event data.  

**GET `/dashboard/settings`**  
- **Description:** Fetches system configuration settings.  
- **Response:** Renders `settings.html` with settings data.  

**POST `/dashboard/settings`**  
- **Description:** Updates system settings if changes are detected.  
- **Response:** `{"success": true, "message": "Paramètre mis à jour avec succès."}` on success, otherwise `{"success": false, "message": "Une erreur est survenue."}`.  


## What is Petzi?
[Petzi](https://www.petzi.ch/) is the Swiss federation of music venues and festivals.

It offers a ticketing service that includes an integrated webhook system.
This webhook sends a JSON payload containing information about purchased tickets to a specified URL,
allowing event organizers to process ticket data in real-time. 

## Screenshots of the app

TODO
