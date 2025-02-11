from flask import Blueprint, request, Response, jsonify

from persistence.database import Database
from service.csv_export import export_table_to_csv
from service.petzi_webhook_handler import insert_ticket

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route("/insert", methods=["POST"])
def insert_message():
    return insert_ticket(request)


@api_blueprint.route('/download_csv')
def download_db_csv():
    csv = export_table_to_csv()

    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=petzi-webhook-export.csv"}
    )

###############################################################################
#                               GET API ROUTES                                #
###############################################################################
# This routes where made in a fast and dirty way

@api_blueprint.route('/buyers', methods=['GET'])
def get_buyers():
    query = "SELECT * FROM buyers"
    return fetch_table_data(query)


@api_blueprint.route('/locations', methods=['GET'])
def get_locations():
    query = "SELECT * FROM locations"
    return fetch_table_data(query)


@api_blueprint.route('/events', methods=['GET'])
def get_events():
    query = "SELECT * FROM events"
    return fetch_table_data(query)


@api_blueprint.route('/tickets', methods=['GET'])
def get_tickets():
    query = "SELECT * FROM tickets"
    return fetch_table_data(query)


@api_blueprint.route('/sessions', methods=['GET'])
def get_sessions():
    query = "SELECT * FROM sessions"
    return fetch_table_data(query)


def fetch_table_data(query):
    """Fetch data from the database and return as JSON."""
    try:
        with Database.get_db_connection() as conn:
            with conn.cursor() as cur:
                # Execute the query
                cur.execute(query)
                rows = cur.fetchall()

                # Get column names
                column_names = [desc[0] for desc in cur.description]

                # Convert rows to a list of dictionaries
                data = [dict(zip(column_names, row)) for row in rows]

                # Return the data as JSON
                return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

