import os
import psycopg2


class Database:

    DB_PARAMS = None
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.DB_PARAMS = {
            "dbname": os.getenv("DB_NAME", "petzi"),
            "user": os.getenv("DB_USER", "petzi"),
            "password": os.getenv("DB_PASS", "petzi"),
            # FOR LOCALHOST HOST, if you want to run flask on your machine instead of the container :
            # "host": os.getenv("DB_HOST", "localhost"),
            # FOR DOCKER :
            "host": os.getenv("DB_HOST", "db"),
            "port": os.getenv("DB_PORT", "5433"),
        }
        return cls._instance


    @staticmethod
    def get_db_connection():
        """Returns a new database connection."""
        return psycopg2.connect(**Database.DB_PARAMS)

    @staticmethod
    def create_tables():
        """Creates necessary tables if they do not exist."""
        with Database.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS buyers (
                        id SERIAL PRIMARY KEY,
                        role VARCHAR(50) NOT NULL,
                        first_name VARCHAR(100) NOT NULL,
                        last_name VARCHAR(100) NOT NULL,
                        postcode VARCHAR(20)
                    );
    
                    CREATE TABLE IF NOT EXISTS locations (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        street VARCHAR(255) NOT NULL,
                        city VARCHAR(100) NOT NULL,
                        postcode VARCHAR(20) NOT NULL
                    );
    
                    CREATE TABLE IF NOT EXISTS events (
                        id SERIAL PRIMARY KEY,
                        event_id INT UNIQUE NOT NULL,
                        name VARCHAR(255) NOT NULL
                    );
    
                    CREATE TABLE IF NOT EXISTS tickets (
                        id SERIAL PRIMARY KEY,
                        number VARCHAR(50) UNIQUE NOT NULL,
                        type VARCHAR(50) NOT NULL,
                        title VARCHAR(255) NOT NULL,
                        category VARCHAR(100),
                        event_id INT REFERENCES events(event_id) ON DELETE CASCADE,
                        cancellation_reason TEXT,
                        generated_at TIMESTAMPTZ NOT NULL,
                        promoter VARCHAR(255) NOT NULL,
                        price_amount DECIMAL(10,2) NOT NULL,
                        price_currency VARCHAR(10) NOT NULL,
                        buyer_id INT REFERENCES buyers(id) ON DELETE SET NULL
                    );
    
                    CREATE TABLE IF NOT EXISTS sessions (
                        id SERIAL PRIMARY KEY,
                        ticket_id INT REFERENCES tickets(id) ON DELETE CASCADE,
                        name VARCHAR(255) NOT NULL,
                        date DATE NOT NULL,
                        time TIME NOT NULL,
                        doors TIME NOT NULL,
                        location_id INT REFERENCES locations(id) ON DELETE CASCADE
                    );
    
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(255) UNIQUE NOT NULL,
                        password VARCHAR(255) NOT NULL
                    );
    
                    CREATE TABLE IF NOT EXISTS web_config (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        value VARCHAR(255) NOT NULL
                    );
                    
                """)

                # Insert initial web config dummy data if the table is empty
                cur.execute("SELECT COUNT(*) FROM web_config;")
                if cur.fetchone()[0] == 0:
                    cur.execute(
                        """
                        INSERT INTO web_config (name, value)
                        VALUES (%s, %s);
                        """,
                        ("shared_petzi_secret", "change-moi!")
                    )

                conn.commit()
