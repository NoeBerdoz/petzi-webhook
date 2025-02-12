import math

import psycopg2
import psycopg2.extras
from flask import render_template, Blueprint, request, redirect, url_for, jsonify

from persistence.database import Database
from routes.auth import login_required
from service.charts import load_last_days_ticket_chart_data

dashboard_blueprint = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_blueprint.route('/home')
@login_required
def get_home():
    with Database.get_db_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT event_id, name FROM events;")
            events = cur.fetchall()

    return render_template('home.html', events=events, title="Accueil")


@dashboard_blueprint.route('/tickets')
@login_required
def get_tickets():
    with Database.get_db_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(
                """
                    SELECT t.id, e.name AS event_name, generated_at, price_amount, buyer_id, promoter, cancellation_reason, price_currency, number, type, title, category
                    FROM tickets t
                    INNER JOIN events e ON e.event_id = t.event_id
                    ORDER BY t.generated_at DESC;
                """
            )
            tickets = [dict(row) for row in cur.fetchall()]

            page = request.args.get('page', 1, type=int)  # Get current page from query params
            per_page = 30
            total_pages = math.ceil(len(tickets) / per_page)

            start = (page - 1) * per_page
            end = start + per_page

            paginated_data = tickets[start:end]

            chart_data = load_last_days_ticket_chart_data()

            return render_template(
                'tickets.html',
                title="Tickets",
                data=paginated_data,
                page=page,
                total_pages=total_pages,
                chart_categories=chart_data["categories"],
                chart_sales=chart_data["sales"],
            )


@dashboard_blueprint.route('/events')
@login_required
def get_events():
    with Database.get_db_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(
                """
                    SELECT 
                        e.id,
                        e.event_id,
                        e.name,
                        COUNT(t.id) AS ticket_count
                    FROM events e
                    LEFT JOIN tickets t ON e.event_id = t.event_id
                    GROUP BY e.id, e.event_id, e.name
                    ORDER BY e.id DESC;
                """
            )
            events = [dict(row) for row in cur.fetchall()]

            page = request.args.get('page', 1, type=int)  # Get current page from query params
            per_page = 30
            total_pages = math.ceil(len(events) / per_page)

            start = (page - 1) * per_page
            end = start + per_page

            paginated_data = events[start:end]

            return render_template(
                'events.html',
                title="Events",
                data=paginated_data,
                events=events,
                page=page,
                total_pages=total_pages,
            )


@dashboard_blueprint.route('/settings')
@login_required
def get_settings():
    with Database.get_db_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(
                """
                    SELECT name, value FROM web_config;
                """
            )
            settings = [dict(row) for row in cur.fetchall()]

            return render_template(
                'settings.html',
                title="Paramètres",
                data=settings,
            )


@dashboard_blueprint.route('/settings', methods=['POST'])
@login_required
def update_settings():
    updated = False
    with Database.get_db_connection() as conn:
        with conn.cursor() as cur:
            for name, new_value in request.form.items():
                cur.execute("SELECT value FROM web_config WHERE name = %s", (name,))
                current_value = cur.fetchone()

                if current_value and current_value[0] != new_value:
                    cur.execute("UPDATE web_config SET value = %s WHERE name = %s", (new_value, name))
                    updated = True

        conn.commit()

    if updated:
        return jsonify({"success": True, "message": "Paramètre mis à jour avec succès."})
    else:
        return jsonify({"success": False, "message": "Une erreur est survenue."})

    return redirect(url_for('dashboard.get_settings'))
