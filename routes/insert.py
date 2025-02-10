from flask import Blueprint, request
from persistence.database import Database
from service.petzi_webhook_handler import insert_ticket

insert_blueprint = Blueprint('insert', __name__)


@insert_blueprint.route("/insert", methods=["POST"])
def insert_message():
    return insert_ticket(request)

