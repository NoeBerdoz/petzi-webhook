from persistence.database import Database
from flask import jsonify

from service.petzi_authenticator import PetziAuthenticator

petzi_authenticator = PetziAuthenticator()


def is_existing_event(event_id):
    with Database.get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                   SELECT event_id FROM events WHERE event_id = '%s';
               """, (event_id, ))
            return cur.fetchone() is not None


def insert_ticket(request):
    """
        Insert webhook related data in one shot.
        TODO divide this part per table concerned.
    """
    if petzi_authenticator.verify_signature(request) is False:
        return False

    data = request.json

    event_data = data.get("details", {}).get("ticket", {})
    buyer_data = data.get("details", {}).get("buyer", {})
    session_data = event_data.get("sessions", [])[0] if event_data.get("sessions") else None
    location_data = session_data.get("location", {}) if session_data else {}
    price_data = event_data.get("price", {})

    if not all([event_data, buyer_data, session_data, location_data, price_data]):
        return jsonify({"error": "Des données sont manquantes dans le message"}), 400

    with Database.get_db_connection() as conn:
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

            cur.execute("""
                   INSERT INTO tickets (number, type, title, category, event_id, cancellation_reason, generated_at, 
                                        promoter, price_amount, price_currency, buyer_id)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
               """, (event_data["number"], event_data["type"], event_data["title"], event_data["category"],
                     event_data["eventId"], event_data["cancellationReason"], event_data["generatedAt"],
                     event_data["promoter"], price_data["amount"], price_data["currency"], buyer_id))
            ticket_id = cur.fetchone()[0]

            cur.execute("""
                   INSERT INTO locations (name, street, city, postcode) 
                   VALUES (%s, %s, %s, %s) RETURNING id;
               """, (location_data["name"], location_data["street"], location_data["city"], location_data["postcode"]))
            location_id = cur.fetchone()[0]

            cur.execute("""
                   INSERT INTO sessions (ticket_id, name, date, time, doors, location_id)
                   VALUES (%s, %s, %s, %s, %s, %s);
               """, (ticket_id, session_data["name"], session_data["date"], session_data["time"],
                     session_data["doors"], location_id))

            conn.commit()

    return jsonify({"message": "Data insert successfully"}), 200