import os

import requests
from dotenv import load_dotenv


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434/api/generate"
)

MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3.2"
)


# ============================================================
# GENERATE ANSWER
# ============================================================

def generate_answer(
    question,
    retrieved_documents
):

    context_parts = []

    for document in retrieved_documents:

        context_parts.append(
            f"""
Source: {document['source']['source']}
Page: {document['source']['page']}

{document['text']}
"""
        )

    context = "\n".join(
        context_parts
    )


    prompt = f"""
You are an HR Policy Assistant.

Answer the employee's question using ONLY the provided
company HR policy context.

Do not invent or assume any company policy.

If the answer cannot be found in the context, say:

"I could not find this information in the provided HR policies."

Keep the answer concise and professional.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""


    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )


    response.raise_for_status()


    return response.json()["response"]