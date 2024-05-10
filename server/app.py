import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError  
from flask_migrate import Migrate
from flask_cors import CORS
# from models import tables

# Set base directory and database URI
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

# Create Flask app
app = Flask(__name__)


CORS(app, resources={r"*": {"origins": "*"}})

# Configure Flask app
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "your_default_secret_key")
app.json.compact = False  # Optional setting for more readable JSON output

# Initialize SQLAlchemy and migrations
db.init_app(app)
migrate = Migrate(app, db)

# Routes