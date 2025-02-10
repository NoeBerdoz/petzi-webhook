import psycopg2
import psycopg2.extras
from flask import render_template, Blueprint

from persistence.database import Database

dashboard_blueprint = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_blueprint.route('/home')
def load_table():
    with Database.get_db_connection() as conn:
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

    return render_template('home.html', data=data, title="My Dashboard")


@dashboard_blueprint.route('/tickets')
def get_tickets():
    with Database.get_db_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(
                """
                    SELECT t.id, e.name AS event_name, generated_at, price_amount, buyer_id, promoter, cancellation_reason, price_currency, number, type, title, category
                    FROM tickets t
                    INNER JOIN events e ON e.event_id = t.event_id;
                """
            )
            tickets = [dict(row) for row in cur.fetchall()]

            return render_template('tickets.html', data=tickets, title="Tickets")
