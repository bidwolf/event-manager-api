from flask import Flask
from flask_cors import CORS

from src.drivers.database.connection import connection

connection.make_connection()
app = Flask(__name__)
CORS(app=app)

from .routes.events import event_blueprint
from .routes.attendees import attendee_blueprint
from .routes.check_ins import check_in_blueprint

app.register_blueprint(event_blueprint)
app.register_blueprint(attendee_blueprint)
app.register_blueprint(check_in_blueprint)
