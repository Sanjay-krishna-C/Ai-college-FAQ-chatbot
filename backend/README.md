# CampusAI Backend

FastAPI-powered backend service for the **CampusAI - Intelligent College Information & FAQ Portal**.

---

## 1. Project Structure

```text
backend/
├── app/
│   ├── main.py                  # FastAPI Application entrypoint & CORS config
│   ├── core/
│   │   ├── config.py            # Pydantic Settings & environment variables
│   │   └── logging.py           # Structured application logging
│   ├── api/
│   │   ├── routes/
│   │   │   ├── health.py        # GET /api/health endpoint
│   │   │   └── chat.py          # POST /api/chat endpoint
│   │   └── router.py            # Central /api prefix router
│   ├── schemas/
│   │   └── chat.py              # Pydantic models for chat requests & RAG sources
│   └── services/
│       └── chat_service.py      # Core chat processing & future RAG orchestration
├── requirements.txt             # Backend dependencies
├── .env.example                 # Environment configuration template
├── .env                         # Local development environment (ignored in git)
└── README.md                    # Setup and API documentation
```

---

## 2. Setup & Installation

### Step A: Create and Activate Python Virtual Environment

```bash
# Navigate to the backend directory
cd backend

# Create virtual environment (Python 3.10+)
python -m venv venv

# Activate virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Windows (Command Prompt):
.\venv\Scripts\activate.bat
# Linux / macOS:
source venv/bin/activate
```

### Step B: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step C: Environment Configuration

Copy `.env.example` to `.env`:

```bash
copy .env.example .env     # Windows
cp .env.example .env       # Linux / macOS
```

Configure your variables inside `.env`:

| Variable | Default Value | Description |
|---|---|---|
| `APP_NAME` | `CampusAI Backend` | Service name |
| `ENVIRONMENT` | `development` | Environment mode (`development` / `production`) |
| `DEBUG` | `True` | Enables Swagger docs at `/docs` |
| `HOST` | `0.0.0.0` | Bind host |
| `PORT` | `8000` | Bind port |
| `CORS_ORIGINS` | `["http://localhost:3000", "http://127.0.0.1:3000"]` | Allowed frontend origins |
| `GEMINI_API_KEY` | *(empty in Phase 5)* | Google Gemini API key (configured in Phase 7) |

---

## 3. Running the Backend Server

Start the development server with auto-reload:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Or run directly with Python:

```bash
python -m app.main
```

- API Base URL: `http://localhost:8000`
- Interactive API Docs (Swagger): `http://localhost:8000/docs`
- Alternative Docs (ReDoc): `http://localhost:8000/redoc`

---

## 4. API Endpoints

### 1. Health Check

- **Endpoint:** `GET /api/health`
- **Description:** Verifies service status and connectivity.
- **Response (`200 OK`):**
  ```json
  {
    "status": "ok",
    "service": "CampusAI Backend"
  }
  ```

### 2. Chat Query

- **Endpoint:** `POST /api/chat`
- **Description:** Processes student inquiries and returns structured AI answers with document citations.
- **Request Body (`application/json`):**
  ```json
  {
    "message": "What is the minimum attendance requirement for semester exams?",
    "conversation_id": "optional-session-id",
    "category": "academics"
  }
  ```
- **Response (`200 OK`):**
  ```json
  {
    "answer": "CampusAI backend is connected successfully. AI retrieval will be enabled in the next phase.",
    "sources": [],
    "mode": "development",
    "session_id": "dev-session"
  }
  ```

---

## 5. Security & Error Handling

- **CORS Protection:** Configured to accept requests exclusively from authorized frontend origins (e.g. `http://localhost:3000`).
- **No Secret Leaks:** API keys and credentials are never hardcoded or echoed back in responses.
- **Sanitized Errors:** Generic HTTP 500 error messages are returned to clients to prevent internal stack trace exposure.
