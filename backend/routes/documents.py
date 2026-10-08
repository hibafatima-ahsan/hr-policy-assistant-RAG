import os

from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required

from rag.ingest import ingest_documents
from utils.auth_utils import admin_required


documents_bp = Blueprint("documents", __name__)

UPLOAD_DIR = "uploads"


# =========================
# Upload Document
# Admin Only
# =========================

@documents_bp.route("/api/documents/upload", methods=["POST"])
@admin_required
def upload_document():

    if "file" not in request.files:
        return jsonify({
            "error": "No file provided"
        }), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({
            "error": "No file selected"
        }), 400

    if not file.filename.lower().endswith(".pdf"):
        return jsonify({
            "error": "Only PDF files are supported"
        }), 400

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    filename = secure_filename(file.filename)

    file_path = os.path.join(
        UPLOAD_DIR,
        filename
    )

    file.save(file_path)

    return jsonify({
        "message": "Document uploaded successfully",
        "filename": filename
    }), 201


# =========================
# Process / Ingest Documents
# Admin Only
# =========================

@documents_bp.route("/api/documents/ingest", methods=["POST"])
@admin_required
def ingest():

    try:

        count = ingest_documents()

        return jsonify({
            "message": "Documents ingested successfully",
            "chunks": count
        })

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


# =========================
# List Documents
# Logged-in Users
# =========================

@documents_bp.route("/api/documents", methods=["GET"])
@jwt_required()
def list_documents():

    try:

        os.makedirs(UPLOAD_DIR, exist_ok=True)

        documents = []

        for filename in os.listdir(UPLOAD_DIR):

            if filename.lower().endswith(".pdf"):

                file_path = os.path.join(
                    UPLOAD_DIR,
                    filename
                )

                file_size = os.path.getsize(
                    file_path
                )

                documents.append({
                    "filename": filename,
                    "size": file_size
                })

        return jsonify({
            "documents": documents
        })

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


# =========================
# Delete Document
# Admin Only
# =========================

@documents_bp.route(
    "/api/documents/<filename>",
    methods=["DELETE"]
)
@admin_required
def delete_document(filename):

    try:

        filename = secure_filename(filename)

        file_path = os.path.join(
            UPLOAD_DIR,
            filename
        )

        if not os.path.exists(file_path):
            return jsonify({
                "error": "Document not found"
            }), 404

        os.remove(file_path)

        # Rebuild the vector database
        try:

            ingest_documents()

        except ValueError:

            # No documents remaining
            vector_dir = "vector_db"

            index_file = os.path.join(
                vector_dir,
                "index.faiss"
            )

            metadata_file = os.path.join(
                vector_dir,
                "metadata.pkl"
            )

            if os.path.exists(index_file):
                os.remove(index_file)

            if os.path.exists(metadata_file):
                os.remove(metadata_file)

        return jsonify({
            "message": "Document deleted successfully"
        })

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500