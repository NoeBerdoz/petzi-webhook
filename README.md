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

## Security
**NOTE:** This project was made as part of a bachelor's course, in a one week rush.  
Therefore, keep in mind that its security is minimal.  
There are potential SQL injection vulnerabilities.

User login is secure, implemented with Werkzeug.  
Passwords are hashed in the database, no plain text storage.

## Screenshots of the app

**_Dashboard Home page_**
lets the user choose an event in the database and dump a csv with all the related tickets from it.
![image](https://github.com/user-attachments/assets/abce3008-487f-46e8-a3b1-e35d5c3404d7)

**_Dashboard Tickets page_**
Table view of the incoming tickets.
![image](https://github.com/user-attachments/assets/647872a0-780a-4b84-9626-eb9b368506c1)
Lazy-loaded navigation.
![image](https://github.com/user-attachments/assets/82f0a2b7-a711-4ca6-a01d-ec3bced626a8)
Tickets selling performance in the last 7 days.
![image](https://github.com/user-attachments/assets/eede1a70-bfa2-4184-9727-0f5463ef5669)

**_Dashboard Events page_**
Table view of the events.
![image](https://github.com/user-attachments/assets/50ad973f-77ef-45db-9354-242516213264)
The user can choose an event to analyze its tickets selling performance.
![image](https://github.com/user-attachments/assets/dbd1cffa-ec0b-487b-a4be-73f7fb24ec9a)

**_Dashboard Settings page_**
The user can change the settings present in the database table `web_config`.
He can set up the shared secret with the Petzi webhook service.
![image](https://github.com/user-attachments/assets/edd73352-d532-4ef3-a2ec-0b07a3402d7b)

**_Login page_**
![image](https://github.com/user-attachments/assets/088e58ce-20a6-40ca-9daa-89fc559af1ef)

**_Register page_**
![image](https://github.com/user-attachments/assets/b33a54c4-2339-4f8a-b94f-1c67d2830802)

**_Logged-in user menu_**
Lets the user Log out or go to the user settings page.
![image](https://github.com/user-attachments/assets/30d66f76-ee38-46db-bd50-9f7ac58c2977)

**_User settings page_**
Lets the user change his password.
![image](https://github.com/user-attachments/assets/8e6e3192-4696-48e3-9d6f-297b4bcd5cc4)

**_Interactions feedbacks_**
![image](https://github.com/user-attachments/assets/17f53dc6-099e-42db-bc0f-0d59fbc5e557)
![image](https://github.com/user-attachments/assets/d4e6ddbc-c4a9-4b4f-aede-c6f8fcd3e5c5)
![image](https://github.com/user-attachments/assets/4253da72-27aa-45ad-8a2a-6799b361a214)

## What is Petzi?
[Petzi](https://www.petzi.ch/) is the Swiss federation of music venues and festivals.

It offers a ticketing service that includes an integrated webhook system.
This webhook sends a JSON payload containing information about purchased tickets to a specified URL,
allowing event organizers to process ticket data in real-time. 

## License
MIT License

Copyright (c) 2025 Noé Berdoz 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.












