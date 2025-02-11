from persistence.database import Database

# TODO make this load only the last few days data
# to avoid performance issue
def load_ticket_chart_data():
    with Database.get_db_connection() as conn:
        with conn.cursor() as cur:
            # Fetch ticket sales per month
            cur.execute("""
                SELECT 
                    DATE_TRUNC('hour', generated_at) AS timestamp,  -- Get full date with hour precision
                    COUNT(id) AS sales_count
                FROM tickets
                GROUP BY timestamp
                ORDER BY timestamp;
            """)
            result = cur.fetchall()

            sales_data = []
            categories = []
            cumulative_sales = 0

            for row in result:
                timestamp = row[0]  # Get the full datetime
                formatted_date = timestamp.strftime("%d.%m %H:00")

                cumulative_sales += row[1]  # Add sales count to cumulative total
                sales_data.append(cumulative_sales)
                categories.append(formatted_date)

            return {"categories": categories, "sales": sales_data}

