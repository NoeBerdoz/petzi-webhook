# petzi-webhook

This is a Flask-based web application designed to store and display Petzi's webhook data.
It allows users to view and manage information received via webhooks in a user-friendly interface. The application uses PostgreSQL for data storage and is containerized using Docker Compose for easy deployment and development.

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

TODO 

## What is Petzi?
[Petzi](https://www.petzi.ch/) is the Swiss federation of music venues and festivals.

It has a ticketing service with an integrated webhook. This webhook sends a JSON
with the informaiton of buyed ticket...

## Screenshots of the app

TODO
