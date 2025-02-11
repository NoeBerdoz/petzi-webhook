from collections import defaultdict

from persistence.database import Database


def load_ticket_chart_data():
    with Database.get_db_connection() as conn:
        with conn.cursor() as cur:
            # Fetch ticket sales per month
            cur.execute("""
                SELECT 
                    EXTRACT(HOUR FROM generated_at) AS hour,
                    EXTRACT(DAY FROM generated_at) AS day,
                    COUNT(id) AS sales_count
                FROM tickets
                GROUP BY day, hour
                ORDER BY day, hour;
            """)
            result = cur.fetchall()

            # Prepare data structure for ApexCharts
            sales_data = defaultdict(int)
            categories = []

            for row in result:
                time_label = f"Day {int(row[1])}, {int(row[0]):02d}:00" # Format as "Day X, HH:00"
                sales_data[time_label] = row[2]
                if time_label not in categories:
                    categories.append(time_label)

            # Sort categories for chronological order
            sorted_categories = categories.sort()

            # Prepare the data for the chart
            sales = [sales_data[category] for category in categories]

            return {"categories": sorted_categories, "sales": sales}