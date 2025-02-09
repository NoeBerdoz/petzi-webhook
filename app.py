import hashlib
import hmac

from flask import Flask, request, jsonify, render_template
import psycopg2
import psycopg2.extras
import os

app = Flask(__name__)

# Configuration de la base de données via les variables d'environnement
DB_PARAMS = {
    "dbname": os.getenv("DB_NAME", "petzi"),
    "user": os.getenv("DB_USER", "petzi"),
    "password": os.getenv("DB_PASS", "petzi"),
    # FOR LOCALHOST HOST
    "host": os.getenv("DB_HOST", "localhost"),
    # FOR DOCKER : "host": os.getenv("DB_HOST", "db"),
    "port": os.getenv("DB_PORT", "5433"),
}


# Connexion à la base de données
def get_db_connection():
    return psycopg2.connect(**DB_PARAMS)


# Création d'une table simple (si elle n'existe pas)
def create_tables():
    with get_db_connection() as conn:
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
                    username VARCHAR(255) NOT NULL,
                    password VARCHAR(255) NOT NULL
                );
                
                CREATE TABLE IF NOT EXISTS web_config (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    value VARCHAR(255) NOT NULL
                );
                
            """)
            conn.commit()

# This is bad, I know, I'm rushing
SHARED_PETZI_SECRET = None
def get_shared_secret():
    global SHARED_PETZI_SECRET

    if SHARED_PETZI_SECRET is None:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # Get secret
                cur.execute(
                    """
                       SELECT value FROM web_config WHERE name = 'shared_petzi_secret';
                   """)
                result = cur.fetchone()
                SHARED_PETZI_SECRET = result[0] if result else None


def verify_signature(request):
    if SHARED_PETZI_SECRET is None: # I'm rushing
        get_shared_secret()

    """Verify the Petzi-Signature header."""
    signature_header = request.headers.get('Petzi-Signature')
    if not signature_header:
        return False

    # Extract timestamp and signature from header
    parts = signature_header.split(',')
    if len(parts) != 2:
        return False

    timestamp_part = parts[0].strip()
    signature_part = parts[1].strip()

    if not timestamp_part.startswith('t=') or not signature_part.startswith('v1='):
        return False

    timestamp = timestamp_part[2:]
    signature = signature_part[3:]

    # Recompute the signature
    body = request.get_data(as_text=True)
    body_to_sign = f'{timestamp}.{body}'.encode()
    # Code smell here with SHARED_PETZI_SECRET that can be None with the bad logic implemented
    computed_signature = hmac.new(SHARED_PETZI_SECRET.encode(), body_to_sign, hashlib.sha256).hexdigest()

    # Compare the signatures
    return hmac.compare_digest(computed_signature, signature)

def is_existing_event(event_id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                   SELECT event_id FROM events WHERE event_id = '%s';
               """, (event_id, ))
            return cur.fetchone() is not None


@app.route("/insert", methods=["POST"])
def insert_message():
    """Insère les données du ticket, de l'acheteur, de l'événement et de la session."""
    if verify_signature(request) is False:
        return False

    data = request.json

    # Extraction des informations
    event_data = data.get("details", {}).get("ticket", {})
    buyer_data = data.get("details", {}).get("buyer", {})
    session_data = event_data.get("sessions", [])[0] if event_data.get("sessions") else None
    location_data = session_data.get("location", {}) if session_data else {}
    price_data = event_data.get("price", {})

    # Vérification des champs requis
    if not all([event_data, buyer_data, session_data, location_data, price_data]):
        return jsonify({"error": "Des données sont manquantes dans le message"}), 400

    # Insertion de l'acheteur
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                   INSERT INTO buyers (role, first_name, last_name, postcode) 
                   VALUES (%s, %s, %s, %s) RETURNING id;
               """, (buyer_data["role"], buyer_data["firstName"], buyer_data["lastName"], buyer_data["postcode"]))
            buyer_id = cur.fetchone()[0]

            # Insert event only if not already present
            if is_existing_event(event_data["eventId"]) is False:
                cur.execute("""
                       INSERT INTO events (event_id, name) 
                       VALUES (%s, %s);
                   """, (event_data["eventId"], event_data["event"]))

            # Insertion du ticket
            cur.execute("""
                   INSERT INTO tickets (number, type, title, category, event_id, cancellation_reason, generated_at, 
                                        promoter, price_amount, price_currency, buyer_id)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
               """, (event_data["number"], event_data["type"], event_data["title"], event_data["category"],
                     event_data["eventId"], event_data["cancellationReason"], event_data["generatedAt"],
                     event_data["promoter"], price_data["amount"], price_data["currency"], buyer_id))
            ticket_id = cur.fetchone()[0]

            # Insertion de la localisation
            cur.execute("""
                   INSERT INTO locations (name, street, city, postcode) 
                   VALUES (%s, %s, %s, %s) RETURNING id;
               """, (location_data["name"], location_data["street"], location_data["city"], location_data["postcode"]))
            location_id = cur.fetchone()[0]

            # Insertion de la session
            cur.execute("""
                   INSERT INTO sessions (ticket_id, name, date, time, doors, location_id)
                   VALUES (%s, %s, %s, %s, %s, %s);
               """, (ticket_id, session_data["name"], session_data["date"], session_data["time"],
                     session_data["doors"], location_id))

            conn.commit()

    return jsonify({"message": "Données insérées avec succès"}), 201

@app.route('/dashboard')
def load_table():
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:

            # Fetch buyers
            cur.execute(
                """
                   SELECT id, role, first_name, last_name, postcode FROM buyers;
               """)
            buyers = [dict(row) for row in cur.fetchall()]

            # Fetch tickets
            cur.execute(
                """
                   SELECT id, number, type, title, category, event_id, cancellation_reason, generated_at, promoter, price_amount, price_currency, buyer_id FROM tickets;
               """)
            tickets = [dict(row) for row in cur.fetchall()]

            # Merge buyers and tickets
            data = []
            for buyer in buyers:
                buyer_tickets = [t for t in tickets if t["buyer_id"] == buyer["id"]]
                data.append({"buyer": buyer, "tickets": buyer_tickets})



    return render_template('dashboard.html', data=data, title="My Dashboard")


if __name__ == "__main__":
    create_tables()  # Crée la table au démarrage
    app.run(host="0.0.0.0", port=5000, debug=True)
