# 🤖 HR Policy Assistant — RAG-Based HR Knowledge Assistant

> An AI-powered HR Policy Assistant that uses **Retrieval-Augmented Generation (RAG)** to answer employee questions from company HR policy documents with grounded, source-aware responses.

---

## 📌 Overview

**HR Policy Assistant** is a full-stack AI application designed to help employees quickly find information from company HR policies.

Instead of relying only on an LLM's general knowledge, the system retrieves relevant information from uploaded HR policy documents and provides the retrieved context to a local LLM before generating an answer.

This reduces hallucinations and keeps responses grounded in the organization's actual HR policies.

### 💡 Example

**Employee asks:**

> How many annual leave days do employees get?

**System retrieves:**

> Annual Leave Policy → Page 1

**AI responds:**

> Employees are entitled to 24 annual leave days per calendar year.

The response also displays the retrieved document source and page.

---

# ✨ Features

### 👤 Authentication & Authorization

* 🔐 Employee registration and login
* 🔑 JWT-based authentication
* 👥 Role-based access control
* 👨‍💼 Employee and Admin roles
* 🛡️ Protected API endpoints
* 🔒 Password hashing

### 📄 HR Document Management

* 📤 Admin-only PDF upload
* 📋 View uploaded HR policy documents
* 🗑️ Admin-only document deletion
* 🔄 Document re-ingestion
* 📚 Support for multiple HR policy documents

### 🧠 RAG Pipeline

* 📑 PDF text extraction using PyPDF
* ✂️ Recursive text chunking
* 🔢 Local sentence-transformer embeddings
* 🗂️ FAISS vector database
* 🔍 Semantic similarity search
* 🎯 Top-K relevant chunk retrieval
* 📊 Similarity threshold filtering
* ♻️ Duplicate chunk filtering

### 🤖 AI Generation

* 🦙 Local Llama 3.2 model
* ⚡ Ollama local inference
* 🧩 Context-aware prompting
* 🚫 Reduced hallucination through grounded context
* 💬 Professional HR responses
* ❓ Handles questions not found in policies

### 💬 Chat

* 💭 Ask HR policy questions
* 📚 View retrieved sources
* 🕐 Store chat history
* 🔄 Reopen previous conversations
* 👤 User-specific chat history

### 🎨 Frontend

* ⚛️ React
* ⚡ Vite
* 📱 Responsive design
* 🖥️ Professional dashboard
* 📄 Document management interface
* 💬 Chat interface
* 🔐 Login interface
* 📊 Source display

---

# 🏗️ System Architecture

```text
                         👤 Employee / Admin
                                │
                                ▼
                     ⚛️ React + Vite Frontend
                                │
                         HTTP / REST API
                                │
                                ▼
                       🐍 Flask Backend
                                │
              ┌─────────────────┼─────────────────┐
              │                 │                 │
              ▼                 ▼                 ▼
        🔐 JWT Auth       📄 Documents       💬 Chat API
              │                 │                 │
              │                 ▼                 │
              │          PDF Extraction           │
              │                 │                 │
              │                 ▼                 │
              │            Text Chunks            │
              │                 │                 │
              │                 ▼                 │
              │       Sentence Transformers       │
              │                 │                 │
              │                 ▼                 │
              │          🗂️ FAISS Index           │
              │                 │                 │
              │                 ▼                 │
              │       🔍 Relevant Chunks           │
              │                 │                 │
              └─────────────────┼─────────────────┘
                                │
                                ▼
                       🦙 Ollama / Llama 3.2
                                │
                                ▼
                         🤖 Grounded Answer
                                │
                    ┌───────────┴───────────┐
                    ▼                       ▼
              📚 Sources              💾 Chat History
                                      SQLite
```

---

# 🧠 How RAG Works

The project uses **Retrieval-Augmented Generation** instead of sending the user's question directly to the LLM.

### 1️⃣ Document Upload

An administrator uploads an HR policy PDF.

```text
annual_leave_policy.pdf
```

### 2️⃣ PDF Extraction

The system extracts text from each PDF page using **PyPDF**.

```text
PDF
 ↓
Page 1 text
Page 2 text
Page 3 text
```

### 3️⃣ Text Chunking

Large documents are divided into smaller chunks using LangChain's recursive text splitter.

```text
Document
   ↓
Chunk 1
Chunk 2
Chunk 3
...
```

Current configuration:

```text
Chunk size: 700 characters
Overlap: 100 characters
```

### 4️⃣ Embeddings

Each chunk is converted into a numerical vector using:

```text
all-MiniLM-L6-v2
```

These embeddings allow the system to compare semantic meaning rather than relying only on exact keywords.

### 5️⃣ FAISS Indexing

The embeddings are stored in a local **FAISS** vector database.

```text
Text Chunk
    ↓
Embedding
    ↓
FAISS Index
```

### 6️⃣ Question Embedding

When an employee asks a question, the question is also converted into an embedding.

```text
User Question
     ↓
Embedding
```

### 7️⃣ Similarity Search

FAISS searches for the most relevant document chunks.

```text
Question
   ↓
FAISS
   ↓
Top relevant chunks
```

The system also applies a similarity threshold to remove weak matches.

### 8️⃣ Context Construction

The retrieved chunks are combined into a context containing:

```text
Source
Page
Relevant text
```

### 9️⃣ LLM Generation

The context and user question are sent to **Llama 3.2 through Ollama**.

The model is instructed to answer using only the provided HR policy context.

### 🔟 Final Response

The system returns:

```text
AI Answer
+
Source Document
+
Page Number
```

---

# 🛠️ Technology Stack

| Layer                    | Technology            |
| ------------------------ | --------------------- |
| 🎨 Frontend              | React                 |
| ⚡ Frontend Tooling       | Vite                  |
| 🐍 Backend               | Python                |
| 🌐 Web Framework         | Flask                 |
| 🔐 Authentication        | Flask-JWT-Extended    |
| 🔒 Password Security     | Werkzeug              |
| 📄 PDF Processing        | PyPDF                 |
| 🧠 Embeddings            | Sentence Transformers |
| 🗂️ Vector Database      | FAISS                 |
| 🔗 RAG Framework         | LangChain             |
| 🤖 LLM                   | Llama 3.2             |
| 🦙 Local LLM Runtime     | Ollama                |
| 💾 Database              | SQLite                |
| 🌍 API Communication     | REST / HTTP           |
| 🔄 Cross-Origin Requests | Flask-CORS            |
| ⚙️ Configuration         | python-dotenv         |
| 📦 Package Management    | pip / npm             |
| 🔧 Version Control       | Git / GitHub          |

---

# 📁 Project Structure

```text
hr-policy-assistant-rag/
│
├── 📁 backend/
│   │
│   ├── 📄 app.py
│   ├── 📄 admin.py
│   ├── 📄 requirements.txt
│   │
│   ├── 📁 database/
│   │   └── auth_db.py
│   │
│   ├── 📁 rag/
│   │   ├── __init__.py
│   │   ├── embeddings.py
│   │   ├── generator.py
│   │   ├── ingest.py
│   │   ├── loader.py
│   │   ├── retriever.py
│   │   ├── splitter.py
│   │   └── vector_store.py
│   │
│   ├── 📁 routes/
│   │   ├── auth.py
│   │   ├── chat.py
│   │   └── documents.py
│   │
│   ├── 📁 utils/
│   │   └── auth_utils.py
│   │
│   └── 📁 uploads/
│
├── 📁 frontend/
│   │
│   ├── 📄 package.json
│   ├── 📄 vite.config.js
│   ├── 📄 index.html
│   │
│   └── 📁 src/
│       ├── App.jsx
│       ├── Login.jsx
│       ├── index.css
│       └── main.jsx
│
├── 📁 data/
│   └── Sample HR policy documents
│
├── 📄 .gitignore
└── 📄 README.md
```

---

# ⚙️ Installation

## 📋 Prerequisites

Install the following:

* 🐍 Python 3.12+
* ⚛️ Node.js
* 📦 npm
* 🦙 Ollama
* 🔧 Git

---

# 🐍 Backend Setup

Navigate to the project:

```bash
cd hr-policy-assistant-rag
```

Go to the backend:

```bash
cd backend
```

Create/activate the Conda environment:

```bash
conda create -n hr-rag python=3.12
conda activate hr-rag
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create:

```text
backend/.env
```

Example:

```env
JWT_SECRET_KEY=your-long-secure-secret-key
OLLAMA_URL=http://localhost:11434/api/generate
OLLAMA_MODEL=llama3.2
```

⚠️ **Never commit `.env` to GitHub.**

---

# 🦙 Ollama Setup

Install Ollama and download Llama 3.2:

```bash
ollama pull llama3.2
```

Check installed models:

```bash
ollama list
```

Test the model:

```bash
ollama run llama3.2
```

---

# 📚 Build the RAG Knowledge Base

Place HR policy PDFs inside:

```text
backend/uploads/
```

Then run:

```bash
python -m rag.ingest
```

Example output:

```text
Processing: annual_leave_policy.pdf
Processing: remote_work_policy.pdf

Successfully created 8 chunks.
```

This creates the local FAISS knowledge base.

---

# ▶️ Start the Backend

From:

```text
backend/
```

run:

```bash
python app.py
```

Backend:

```text
http://127.0.0.1:5000
```

---

# ⚛️ Start the Frontend

Open another terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start Vite:

```bash
npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

# 🔐 User Roles

## 👤 Employee

Employees can:

* Login
* Ask HR policy questions
* View AI responses
* View retrieved sources
* View chat history

## 👨‍💼 Admin

Admins can additionally:

* Upload HR policy PDFs
* View uploaded documents
* Delete documents
* Rebuild the RAG knowledge base

---

# 🔌 API Endpoints

## 🔐 Authentication

### Register

```http
POST /api/auth/register
```

Example:

```json
{
  "name": "Hiba",
  "email": "user@example.com",
  "password": "password123"
}
```

### Login

```http
POST /api/auth/login
```

### Current User

```http
GET /api/auth/me
Authorization: Bearer <JWT>
```

---

## 📄 Documents

### Upload PDF

```http
POST /api/documents/upload
Authorization: Bearer <ADMIN_JWT>
```

### Process Documents

```http
POST /api/documents/ingest
Authorization: Bearer <ADMIN_JWT>
```

### List Documents

```http
GET /api/documents
Authorization: Bearer <JWT>
```

### Delete Document

```http
DELETE /api/documents/<filename>
Authorization: Bearer <ADMIN_JWT>
```

---

## 💬 Chat

### Ask Question

```http
POST /api/chat
Authorization: Bearer <JWT>
```

Example:

```json
{
  "question": "How many annual leave days do employees get?"
}
```

### Chat History

```http
GET /api/chat/history
Authorization: Bearer <JWT>
```

---

# 🧪 Example Questions

### ✅ Question Found in Policy

```text
How many annual leave days do employees get?
```

Example response:

```text
Employees are entitled to 24 annual leave days per calendar year.
```

Source:

```text
annual_leave_policy.pdf
Page 1
```

---

### ✅ Multi-Document Retrieval

```text
How many days can employees work remotely per week?
```

The system retrieves information from the remote-work policy instead of the annual-leave policy.

---

### ❌ Information Not Found

```text
What is the company's car allowance policy?
```

The system responds:

```text
I could not find this information in the provided HR policies.
```

This prevents the model from inventing unsupported company policies.

---

# 🛡️ Security

The project includes:

* 🔐 JWT authentication
* 🔑 Password hashing
* 👥 Role-based authorization
* 🛡️ Admin-only document management
* 🔒 Environment-based secrets
* 🚫 `.env` excluded from Git
* 🚫 SQLite database excluded from Git
* 🚫 Generated FAISS files excluded from Git
* 🚫 Uploaded documents excluded from Git

For production deployment, additional security measures should include:

* Strong production secrets
* HTTPS
* Secure CORS configuration
* Rate limiting
* File size/type validation
* Secure production database
* Secure LLM infrastructure
* Proper secret management

---

# 🚀 Deployment

The current development configuration uses:

```text
Ollama → localhost:11434
```

This works locally because Ollama is running on the developer's computer.

For cloud deployment, the LLM must be made accessible to the deployed backend through a suitable hosted inference service or remotely accessible model server.

A production architecture can therefore be:

```text
⚛️ React / Vercel
        │
        ▼
🐍 Flask API / Cloud Server
        │
        ├── 🔐 Authentication
        ├── 📚 RAG Pipeline
        ├── 🗂️ Vector Database
        │
        ▼
☁️ Hosted LLM / Remote Inference
```

---

# 📈 Future Improvements

The current application provides the complete core RAG workflow. Possible future improvements include:

* 🌐 Production cloud deployment
* 🗃️ PostgreSQL/Supabase database
* ☁️ Cloud vector database
* 📊 Admin analytics dashboard
* 👥 Employee management
* 🏢 Company-specific knowledge bases
* 📄 DOCX support
* 📑 More document formats
* 🔎 Advanced hybrid search
* 🧠 Reranking models
* 💬 Streaming AI responses
* 📱 Improved mobile UI
* 🔔 Notifications
* 📈 Usage analytics
* 🧪 Automated backend/API testing
* 🔄 CI/CD with GitHub Actions

---

# 🧪 Testing

The project includes retrieval testing scripts.

Example:

```bash
python test_retrieval.py
```

Example retrieval result:

```text
Source: annual_leave_policy.pdf
Page: 1
Similarity Score: 0.60+
```

The system has been tested with:

* 📄 Single-document retrieval
* 📚 Multi-document retrieval
* 🔍 Semantic search
* 🤖 LLM answer generation
* 🔐 Authentication
* 👥 Role-based access
* 💬 Chat history
* ❌ Unknown-policy questions

---

# 🎯 Project Objectives

The project was developed to demonstrate practical implementation of:

* Retrieval-Augmented Generation
* Semantic document search
* Vector databases
* Local LLM inference
* Full-stack web development
* REST API development
* Authentication and authorization
* AI-powered enterprise applications
* Document-based question answering

---

# 🧠 Key Concepts Demonstrated

### Artificial Intelligence

* Large Language Models
* Prompt Engineering
* Retrieval-Augmented Generation
* Embeddings
* Semantic Search
* Context Grounding

### Backend Development

* Python
* Flask
* REST APIs
* JWT Authentication
* Role-Based Access Control
* SQLite
* Environment Configuration

### AI Engineering

* LangChain
* Sentence Transformers
* FAISS
* Ollama
* Llama 3.2
* Document Chunking
* Similarity Search

### Frontend Development

* React
* Vite
* JavaScript
* REST API integration
* State management
* Responsive CSS

---

# 📊 RAG Pipeline Summary

```text
📄 HR Policy PDF
       ↓
📑 PyPDF
       ↓
✂️ Text Chunking
       ↓
🧠 Sentence Transformer
       ↓
🔢 Embeddings
       ↓
🗂️ FAISS Vector Store
       ↓
❓ Employee Question
       ↓
🧠 Question Embedding
       ↓
🔍 Similarity Search
       ↓
📚 Relevant Context
       ↓
🦙 Llama 3.2
       ↓
🤖 Grounded Answer
       ↓
📄 Source + Page
       ↓
💾 Chat History
```

---

# 👩‍💻 Author

**Hiba Fatima Ahsan**

🎓 BS Computer Science

💻 Full-Stack Development | AI/ML | RAG | Python | React

---

# ⭐ Project Status

🟢 **Core application completed**

The application currently supports:

```text
✅ Authentication
✅ Role-based access
✅ PDF document management
✅ Multi-document ingestion
✅ Embeddings
✅ FAISS vector search
✅ RAG pipeline
✅ Local LLM generation
✅ Source-aware responses
✅ Chat history
✅ Responsive UI
```

🚧 **Cloud deployment is the next production phase.**

---

# 📄 License

This project is intended for educational, portfolio, and demonstration purposes.

© 2026 Hiba Fatima Ahsan. All rights reserved.
