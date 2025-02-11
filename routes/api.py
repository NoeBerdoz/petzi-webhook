from flask import Blueprint, request, Response, jsonify

from persistence.database import Database
from service.csv_export import export_tables_to_csv
from service.petzi_webhook_handler import insert_ticket

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route("/insert", methods=["POST"])
def insert_message():
    return insert_ticket(request)

@api_blueprint.route('/chart/tickets/<int:event_id>', methods=['GET'])
def get_tickets_by_event(event_id):
    """ Returns data in a format for an apexchart.js component """
    # TODO Handle SQL injection security issue
    with Database.get_db_connection() as conn:
        with conn.cursor() as cur:
            # Fetch ticket data for the selected event
            query = """
                SELECT 
                    DATE_TRUNC('hour', generated_at) AS timestamp,
                    COUNT(id) AS sales_count
                FROM tickets
                WHERE event_id = %s
                GROUP BY timestamp
                ORDER BY timestamp;
            """
            cur.execute(query, (event_id,))
            rows = cur.fetchall()

            # Format the data for the chart
            sales_data = []
            categories = []
            cumulative_sales = 0

            for row in rows:
                timestamp = row[0]  # Get the full datetime
                formatted_date = timestamp.strftime("%d.%m %H:00")

                cumulative_sales += row[1]  # Add sales count to cumulative total
                sales_data.append(cumulative_sales)
                categories.append(formatted_date)

            return jsonify({"categories": categories, "sales": sales_data})


@api_blueprint.route('/download_csv')
def download_db_csv():
    # query parameter in the URL, e.g., /download_csv?event_id=123.
    event_id = request.args.get('event_id')

    if not event_id or not event_id.isdigit():
        return Response(status=400)

    csv = export_tables_to_csv(event_id)

    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename=event_{event_id}_export.csv"}
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


def fetch_table_data(query, params=None):
    """Fetch data from the database and return as JSON."""
    try:
        with Database.get_db_connection() as conn:
            with conn.cursor() as cur:
                # Execute the query with or without parameters
                if params:
                    cur.execute(query, params)
                else:
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

