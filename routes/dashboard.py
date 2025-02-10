import psycopg2
import psycopg2.extras
from flask import render_template, Blueprint

from persistence.database import Database

dashboard_blueprint = Blueprint('dashboard', __name__)

@dashboard_blueprint.route('/dashboard')
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



    return render_template('dashboard.html', data=data, title="My Dashboard")