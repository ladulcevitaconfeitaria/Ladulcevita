# -*- coding: utf-8 -*-
"""Main application file for the client interface."""

import sys
import os
# Ensure the application root is in the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, Blueprint, render_template, redirect, url_for # Added redirect, url_for
from flask_login import LoginManager, current_user, login_required # Added current_user, login_required

# Assuming blueprints are defined in these files - adjust if names differ
try:
    from src.auth import auth_bp
except ImportError:
    print("WARNING: Could not import auth_bp from src.auth", file=sys.stderr)
    auth_bp = None
try:
    # Assuming user.py contains the dashboard and profile routes
    from src.user import user_bp
except ImportError:
    print("WARNING: Could not import user_bp from src.user", file=sys.stderr)
    user_bp = None

# Define the main Flask application instance
app = Flask(__name__)

# --- Configuration (Essential for Login & DB) ---
# Load secret key from environment or set a default (CHANGE THIS IN PRODUCTION)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "a_very_secret_key_for_la_dulce_vita")

# --- Database Configuration (Using SQLite for local testing) ---
# Comment out MySQL configuration
# db_user = os.getenv("DB_USERNAME", "default_user") # Default values for local testing if needed
# db_pass = os.getenv("DB_PASSWORD", "default_password")
# db_host = os.getenv("DB_HOST", "localhost")
# db_port = os.getenv("DB_PORT", "3306")
# db_name = os.getenv("DB_NAME", "default_db")
# app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

# Configure SQLite database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "../instance/local_test.db") # Store DB in instance folder
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Ensure instance folder exists
instance_path = os.path.join(basedir, "../instance")
os.makedirs(instance_path, exist_ok=True)

# --- Database Initialization ---
try:
    from src.models import db
    db.init_app(app)
except ImportError:
    print("ERROR: Could not import or initialize db from src.models", file=sys.stderr)
    # Optionally, raise an error or exit if DB is critical
    db = None
except Exception as e:
    print(f"ERROR initializing database: {e}", file=sys.stderr)
    db = None

# --- Login Manager Initialization ---
login_manager = LoginManager()
login_manager.login_view = "auth.login"  # Route name for the login page (BlueprintName.ViewFunctionName)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    """Loads user object for Flask-Login."""
    try:
        # Import User model here to avoid circular imports if models imports app
        from src.models import User
        return User.query.get(int(user_id))
    except ImportError:
        print("ERROR: Could not import User model from src.models for user_loader", file=sys.stderr)
        return None
    except Exception as e:
        print(f"ERROR in user_loader: {e}", file=sys.stderr)
        return None

# --- Blueprint Registration ---
main_bp = Blueprint("main", __name__, template_folder="templates", static_folder="static")

@main_bp.route("/")
def index():
    """Renders the homepage."""
    # current_user is now available in the template context via Flask-Login
    return render_template("index.html")

@main_bp.route("/benefits")
def benefits():
    """Renders the page explaining the loyalty program benefits and rules."""
    return render_template("benefits.html")

# Add a simple dashboard route (move to user.py later if needed)
@main_bp.route("/dashboard")
@login_required # Protect this route
def dashboard():
    """Renders the user dashboard after login."""
    # Pass current_user to the template (Flask-Login does this automatically, but explicit is fine)
    # A simple dashboard template is needed
    return render_template("dashboard.html", user=current_user)

app.register_blueprint(main_bp)
if auth_bp:
    # The prefix "/auth" was already added in auth.py, no need to add it here again
    app.register_blueprint(auth_bp)
if user_bp:
    # Assuming user_bp handles routes like /profile
    app.register_blueprint(user_bp, url_prefix="/user")

# --- Database Creation (For first run with SQLite) ---
with app.app_context():
    if db is not None:
        try:
            db.create_all()
            print("Database tables created (if they didn't exist).")
        except Exception as e:
            print(f"Error creating database tables: {e}", file=sys.stderr)

# --- Main Execution (for local testing, not used by deploy service) ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
