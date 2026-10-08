import { useEffect, useState } from "react";
import Login from "./Login";

function App() {
  // ============================================================
  // AUTHENTICATION
  // ============================================================

  const [user, setUser] = useState(() => {
    const savedUser = localStorage.getItem("user");

    try {
      return savedUser ? JSON.parse(savedUser) : null;
    } catch {
      localStorage.removeItem("user");
      return null;
    }
  });

  // ============================================================
  // HR ASSISTANT STATE
  // ============================================================

  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);

  // ============================================================
  // DOCUMENT STATE
  // ============================================================

  const [file, setFile] = useState(null);
  const [uploadMessage, setUploadMessage] = useState("");
  const [documents, setDocuments] = useState([]);
  const [documentsLoading, setDocumentsLoading] = useState(false);

  // ============================================================
  // CHAT HISTORY STATE
  // ============================================================

  const [history, setHistory] = useState([]);
  const [historyLoading, setHistoryLoading] = useState(false);

  // ============================================================
  // LOADING STATE
  // ============================================================

  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [ingesting, setIngesting] = useState(false);

  // ============================================================
  // LOAD DOCUMENTS
  // ============================================================

  const loadDocuments = async () => {
    setDocumentsLoading(true);

    try {
      const token = localStorage.getItem("token");

      const response = await fetch(
        "http://127.0.0.1:5000/api/documents",
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.error || "Failed to load documents"
        );
      }

      setDocuments(data.documents || []);
    } catch (error) {
      console.error(
        "Failed to load documents:",
        error
      );
    } finally {
      setDocumentsLoading(false);
    }
  };

  // ============================================================
  // LOAD CHAT HISTORY
  // ============================================================

  const loadChatHistory = async () => {
    setHistoryLoading(true);

    try {
      const token = localStorage.getItem("token");

      const response = await fetch(
        "http://127.0.0.1:5000/api/chat/history",
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.error || "Failed to load chat history"
        );
      }

      setHistory(data.history || []);
    } catch (error) {
      console.error(
        "Failed to load chat history:",
        error
      );
    } finally {
      setHistoryLoading(false);
    }
  };

  // ============================================================
  // LOAD DATA AFTER LOGIN
  // ============================================================

  useEffect(() => {
    if (user) {
      loadDocuments();
      loadChatHistory();
    }
  }, [user]);

  // ============================================================
  // LOGOUT
  // ============================================================

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");

    setUser(null);
    setQuestion("");
    setAnswer("");
    setSources([]);
    setHistory([]);
    setDocuments([]);
  };

  // ============================================================
  // UPLOAD DOCUMENT
  // ============================================================

  const uploadDocument = async () => {
    if (!file) {
      setUploadMessage(
        "Please select a PDF first."
      );
      return;
    }

    setUploading(true);
    setUploadMessage("");

    try {
      const token = localStorage.getItem("token");

      const formData = new FormData();

      formData.append("file", file);

      const response = await fetch(
        "http://127.0.0.1:5000/api/documents/upload",
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
          },
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.error || "Upload failed"
        );
      }

      setUploadMessage(
        `✓ ${data.filename} uploaded successfully.`
      );

      setFile(null);

      const fileInput =
        document.getElementById("fileInput");

      if (fileInput) {
        fileInput.value = "";
      }

      loadDocuments();
    } catch (error) {
      setUploadMessage(
        `Error: ${error.message}`
      );
    } finally {
      setUploading(false);
    }
  };

  // ============================================================
  // PROCESS / INGEST DOCUMENTS
  // ============================================================

  const ingestDocuments = async () => {
    setIngesting(true);

    setUploadMessage(
      "Processing HR documents..."
    );

    try {
      const token = localStorage.getItem("token");

      const response = await fetch(
        "http://127.0.0.1:5000/api/documents/ingest",
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.error || "Ingestion failed"
        );
      }

      setUploadMessage(
        `✓ Documents processed successfully. ${data.chunks} chunks created.`
      );
    } catch (error) {
      setUploadMessage(
        `Error: ${error.message}`
      );
    } finally {
      setIngesting(false);
    }
  };

  // ============================================================
  // DELETE DOCUMENT
  // ============================================================

  const deleteDocument = async (filename) => {
    const confirmed = window.confirm(
      `Delete ${filename}?`
    );

    if (!confirmed) {
      return;
    }

    try {
      const token = localStorage.getItem("token");

      const response = await fetch(
        `http://127.0.0.1:5000/api/documents/${encodeURIComponent(
          filename
        )}`,
        {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.error ||
            "Failed to delete document"
        );
      }

      setUploadMessage(
        `✓ ${filename} deleted successfully.`
      );

      loadDocuments();
    } catch (error) {
      setUploadMessage(
        `Error: ${error.message}`
      );
    }
  };

  // ============================================================
  // ASK HR ASSISTANT
  // ============================================================

  const askQuestion = async () => {
    if (!question.trim()) {
      return;
    }

    setLoading(true);
    setAnswer("");
    setSources([]);

    try {
      const token = localStorage.getItem("token");

      const response = await fetch(
        "http://127.0.0.1:5000/api/chat",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            question: question.trim(),
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.error ||
            "Something went wrong"
        );
      }

      setAnswer(data.answer);
      setSources(data.sources || []);

      // Refresh chat history after successful answer
      loadChatHistory();
    } catch (error) {
      setAnswer(
        `Error: ${error.message}`
      );
    } finally {
      setLoading(false);
    }
  };

  // ============================================================
  // USE HISTORY ITEM
  // ============================================================

  const openHistoryItem = (item) => {
    setQuestion(item.question);
    setAnswer(item.answer);
    setSources([]);
  };

  // ============================================================
  // LOGIN SCREEN
  // ============================================================

  if (!user) {
    return <Login onLogin={setUser} />;
  }

  // ============================================================
  // MAIN DASHBOARD
  // ============================================================

  return (
    <div className="app">

      {/* ======================================================
          HEADER
      ====================================================== */}

      <header className="header">

        <div>
          <h1>
            HR Policy Assistant
          </h1>

          <p>
            AI-powered document-based HR
            policy assistant
          </p>
        </div>

        <div className="status-badge">
          ● AI Assistant Online
        </div>

      </header>

      {/* ======================================================
          USER SECTION
      ====================================================== */}

      <div className="user-section">

        <div>
          <strong>
            {user.name}
          </strong>

          <span>
            {" "}({user.role})
          </span>
        </div>

        <button
          className="logout-button"
          onClick={handleLogout}
        >
          Logout
        </button>

      </div>

      <main className="container">

        {/* ====================================================
            ADMIN DOCUMENT MANAGEMENT
        ==================================================== */}

        {user.role === "admin" && (

          <section className="card">

            <div className="section-title">

              <div>

                <h2>
                  HR Policy Documents
                </h2>

                <p>
                  Upload company HR policy
                  PDFs to build the
                  knowledge base.
                </p>

              </div>

            </div>

            {/* Upload Area */}

            <div className="upload-area">

              <input
                type="file"
                accept=".pdf"
                id="fileInput"
                onChange={(e) =>
                  setFile(
                    e.target.files[0]
                  )
                }
              />

              <label
                htmlFor="fileInput"
                className="file-label"
              >

                📄

                <span>
                  {file
                    ? file.name
                    : "Choose an HR policy PDF"}
                </span>

              </label>

              <div className="button-group">

                <button
                  onClick={uploadDocument}
                  disabled={uploading}
                >
                  {uploading
                    ? "Uploading..."
                    : "Upload PDF"}
                </button>

                <button
                  className="secondary-button"
                  onClick={
                    ingestDocuments
                  }
                  disabled={ingesting}
                >
                  {ingesting
                    ? "Processing..."
                    : "Process Documents"}
                </button>

              </div>

              {uploadMessage && (

                <div className="status-message">
                  {uploadMessage}
                </div>

              )}

            </div>

            {/* Uploaded Documents */}

            <div className="document-list">

              <h3>
                Uploaded Documents
              </h3>

              {documentsLoading ? (

                <p>
                  Loading documents...
                </p>

              ) : documents.length === 0 ? (

                <p>
                  No HR policy documents
                  uploaded.
                </p>

              ) : (

                documents.map(
                  (document) => (

                    <div
                      className="document-item"
                      key={
                        document.filename
                      }
                    >

                      <div>

                        <strong>
                          📄{" "}
                          {document.filename}
                        </strong>

                        <span>
                          {(
                            document.size /
                            1024
                          ).toFixed(1)}{" "}
                          KB
                        </span>

                      </div>

                      <button
                        className="delete-button"
                        onClick={() =>
                          deleteDocument(
                            document.filename
                          )
                        }
                      >
                        Delete
                      </button>

                    </div>

                  )
                )

              )}

            </div>

          </section>

        )}

        {/* ====================================================
            EMPLOYEE INFORMATION
        ==================================================== */}

        {user.role !== "admin" && (

          <section className="card employee-info">

            <h2>
              Welcome, {user.name}
            </h2>

            <p>
              You can ask questions about
              the company's HR policies
              using the AI assistant below.
            </p>

          </section>

        )}

        {/* ====================================================
            ASK HR ASSISTANT
        ==================================================== */}

        <section className="card">

          <div className="section-title">

            <div>

              <h2>
                Ask HR Assistant
              </h2>

              <p>
                Ask questions about the
                uploaded company policies.
              </p>

            </div>

          </div>

          <textarea
            value={question}
            onChange={(e) =>
              setQuestion(e.target.value)
            }
            placeholder="Example: How many annual leave days do employees get?"
          />

          <button
            className="ask-button"
            onClick={askQuestion}
            disabled={loading}
          >
            {loading
              ? "AI is analyzing the HR policy..."
              : "Ask Question →"}
          </button>

        </section>

        {/* ====================================================
            AI RESPONSE
        ==================================================== */}

        {answer && (

          <section className="card answer-card">

            <h2>
              AI Response
            </h2>

            <div className="answer">
              {answer}
            </div>

            {/* Sources */}

            {sources.length > 0 && (

              <div className="sources">

                <h3>
                  Retrieved Sources
                </h3>

                {sources.map(
                  (source, index) => (

                    <div
                      className="source-item"
                      key={index}
                    >

                      <strong>
                        📄{" "}
                        {source.source}
                      </strong>

                      <span>
                        Page{" "}
                        {source.page}
                      </span>

                    </div>

                  )
                )}

              </div>

            )}

          </section>

        )}

        {/* ====================================================
            CHAT HISTORY
        ==================================================== */}

        <section className="card history-card">

          <div className="section-title">

            <div>

              <h2>
                Chat History
              </h2>

              <p>
                Your previous HR policy
                questions and answers.
              </p>

            </div>

          </div>

          {historyLoading ? (

            <p>
              Loading chat history...
            </p>

          ) : history.length === 0 ? (

            <p>
              No previous conversations yet.
            </p>

          ) : (

            <div className="history-list">

              {history.map((item) => (

                <div
                  className="history-item"
                  key={item.id}
                  onClick={() =>
                    openHistoryItem(item)
                  }
                >

                  <div className="history-question">

                    <strong>
                      Q:
                    </strong>

                    <span>
                      {item.question}
                    </span>

                  </div>

                  <div className="history-answer">

                    <strong>
                      A:
                    </strong>

                    <span>
                      {item.answer}
                    </span>

                  </div>

                  <div className="history-date">

                    {item.created_at}

                  </div>

                </div>

              ))}

            </div>

          )}

        </section>

      </main>

      {/* ======================================================
          FOOTER
      ====================================================== */}

      <footer>

        HR Policy Assistant • RAG +
        FAISS + Llama 3.2

      </footer>

    </div>
  );
}

export default App;