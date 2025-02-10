from flask import Flask
from routes.dashboard import dashboard_blueprint
from routes.insert import insert_blueprint
from persistence.database import Database

database = Database()
app = Flask(__name__)
app.register_blueprint(dashboard_blueprint)
app.register_blueprint(insert_blueprint)

if __name__ == "__main__":
    database.create_tables()
    app.run(host="0.0.0.0", port=5000, debug=True)
