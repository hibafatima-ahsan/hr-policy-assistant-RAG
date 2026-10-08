from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from database.auth_db import get_connection
from rag.retriever import retrieve_documents
from rag.generator import generate_answer


chat_bp = Blueprint("chat", __name__)


# ============================================================
# ASK HR ASSISTANT
# ============================================================

@chat_bp.route("/api/chat", methods=["POST"])
@jwt_required()
def chat():

    data = request.get_json()

    if not data or "question" not in data:
        return jsonify({
            "error": "Question is required"
        }), 400

    question = data["question"].strip()

    if not question:
        return jsonify({
            "error": "Question cannot be empty"
        }), 400

    try:

        print("\n==============================")
        print("QUESTION:", question)

        # Retrieve relevant policy chunks
        results = retrieve_documents(
            question,
            top_k=3,
            similarity_threshold=0.35
        )

        print(
            "RETRIEVED RESULTS:",
            len(results)
        )

        for result in results:
            print(
                "SOURCE:",
                result["source"],
                "SCORE:",
                result["score"]
            )

        # No relevant policy found
        if not results:

            print(
                "NO RELEVANT RESULTS FOUND"
            )

            return jsonify({
                "question": question,
                "answer": (
                    "I could not find this information "
                    "in the provided HR policies."
                ),
                "sources": []
            })

        # Generate answer using Ollama
        print("GENERATING ANSWER...")

        answer = generate_answer(
            question,
            results
        )

        print("ANSWER GENERATED")

        # ====================================================
        # SAVE CHAT HISTORY
        # ====================================================

        user_id = get_jwt_identity()

        connection = get_connection()

        connection.execute(
            """
            INSERT INTO chat_history
            (user_id, question, answer)
            VALUES (?, ?, ?)
            """,
            (
                user_id,
                question,
                answer
            )
        )

        connection.commit()
        connection.close()

        print("CHAT HISTORY SAVED")

        # ====================================================
        # PREPARE SOURCES
        # ====================================================

        sources = []

        for result in results:

            sources.append({
                "source": result["source"]["source"],
                "page": result["source"]["page"],
                "score": round(
                    result["score"],
                    4
                )
            })

        print("==============================\n")

        return jsonify({
            "question": question,
            "answer": answer,
            "sources": sources
        })

    except Exception as error:

        print("\nCHAT ERROR:")
        print(error)

        return jsonify({
            "error": str(error)
        }), 500


# ============================================================
# GET CHAT HISTORY
# ============================================================

@chat_bp.route(
    "/api/chat/history",
    methods=["GET"]
)
@jwt_required()
def chat_history():

    try:

        user_id = get_jwt_identity()

        connection = get_connection()

        history = connection.execute(
            """
            SELECT id, question, answer, created_at
            FROM chat_history
            WHERE user_id = ?
            ORDER BY created_at DESC
            """,
            (user_id,)
        ).fetchall()

        connection.close()

        return jsonify({
            "history": [
                {
                    "id": item["id"],
                    "question": item["question"],
                    "answer": item["answer"],
                    "created_at": item["created_at"]
                }
                for item in history
            ]
        })

    except Exception as error:

        print("\nHISTORY ERROR:")
        print(error)

        return jsonify({
            "error": str(error)
        }), 500