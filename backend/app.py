import os

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

from routes.chat import chat_bp
from routes.documents import documents_bp
from routes.auth import auth_bp

from database.auth_db import init_db


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# CREATE FLASK APP
# ============================================================

app = Flask(__name__)


# ============================================================
# JWT CONFIGURATION
# ============================================================

app.config["JWT_SECRET_KEY"] = os.getenv(
    "JWT_SECRET_KEY"
)

if not app.config["JWT_SECRET_KEY"]:
    raise RuntimeError(
        "JWT_SECRET_KEY is not configured in .env"
    )


JWTManager(app)


# ============================================================
# CORS
# ============================================================

CORS(app)


# ============================================================
# DATABASE
# ============================================================

init_db()


# ============================================================
# REGISTER BLUEPRINTS
# ============================================================

app.register_blueprint(chat_bp)
app.register_blueprint(documents_bp)
app.register_blueprint(auth_bp)


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    return {
        "message": "HR Policy Assistant API is running"
    }


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )