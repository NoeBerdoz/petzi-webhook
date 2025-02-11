from flask import Blueprint, request, Response
from service.csv_export import export_table_to_csv
from service.petzi_webhook_handler import insert_ticket

api_blueprint = Blueprint('api', __name__)


# TODO permettre la récupération des data
# par un service externe avec une route GET

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

