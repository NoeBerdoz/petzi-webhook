import csv
import io

from persistence.database import Database


def export_table_to_csv():
    """Fetch table data and return as CSV string."""

    # Define the SQL query to join all tables
    query = """
        SELECT 
            t.number AS ticket_number,
            t.type AS ticket_type,
            t.title AS ticket_title,
            t.category AS ticket_category,
            t.cancellation_reason,
            t.generated_at,
            t.promoter,
            t.price_amount,
            t.price_currency,
            b.role AS buyer_role,
            b.first_name AS buyer_first_name,
            b.last_name AS buyer_last_name,
            b.postcode AS buyer_postcode,
            e.name AS event_name,
            e.event_id AS event_id,
            s.name AS session_name,
            s.date AS session_date,
            s.time AS session_time,
            s.doors AS session_doors,
            l.name AS location_name,
            l.street AS location_street,
            l.city AS location_city,
            l.postcode AS location_postcode
        FROM tickets t
        INNER JOIN buyers b ON t.buyer_id = b.id
        INNER JOIN events e ON t.event_id = e.event_id
        INNER JOIN sessions s ON t.id = s.ticket_id
        INNER JOIN locations l ON s.location_id = l.id
        """

    # Connect to the database
    with Database.get_db_connection() as conn:
        with conn.cursor() as cur:
            # Execute the query
            cur.execute(query)
            rows = cur.fetchall()

            column_names = [desc[0] for desc in cur.description]

            # Create a CSV string
            output = io.StringIO()
            writer = csv.writer(output)

            # Write the header
            writer.writerow(column_names)

            # Write the data rows
            writer.writerows(rows)

            csv_string = output.getvalue()

    return csv_string

