import os

from flask import Flask

from routes.auth import auth_blueprint
from routes.dashboard import dashboard_blueprint
from routes.api import api_blueprint
from persistence.database import Database

database = Database()
app = Flask(__name__)
app.register_blueprint(dashboard_blueprint)
app.register_blueprint(api_blueprint)
app.register_blueprint(auth_blueprint)

if __name__ == "__main__":
    database.create_tables()
    app.secret_key = 'I want to play guitar' # Used by werkzeug to manage authentication
    app.run(host="0.0.0.0", port=5000, debug=True)
