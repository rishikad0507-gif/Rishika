# AI FAQ Assistant API

A beginner-friendly AI-Augmented Backend Development project.

## 1. Project idea

The AI FAQ Assistant stores frequently asked questions in SQLite.
A student can:
- Ask a question
- Get an answer from the FAQ database
- Use an AI fallback when an OpenAI API key is configured
- Add new FAQs
- Delete FAQs

## 2. Technology

- Python
- FastAPI
- SQLite
- HTML/CSS/JavaScript
- Optional OpenAI API

## 3. Setup

Open a terminal inside this project folder.

### Create virtual environment

Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Install packages

```bash
pip install -r requirements.txt
```

### Run

```bash
uvicorn app.main:app --reload
```

Open:
http://127.0.0.1:8000

Swagger API documentation:
http://127.0.0.1:8000/docs

## 4. Optional AI setup

Copy `.env.example` to `.env` and add your API key.

The project still works without an AI key because it uses the local FAQ database and fallback response.

## 5. API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | /api/faqs | View all FAQs |
| POST | /api/faqs | Add an FAQ |
| DELETE | /api/faqs/{id} | Delete an FAQ |
| POST | /api/ask | Ask the assistant |

## 6. Example

POST `/api/ask`

```json
{
  "question": "What is DBMS?"
}
```

Response:

```json
{
  "answer": "DBMS is software used to create, store and manage databases.",
  "source": "FAQ database",
  "category": "Database"
}
```

## 7. Viva explanation

The frontend sends HTTP requests to the FastAPI backend.
The backend checks the SQLite FAQ database.
If a matching FAQ is found, it returns the stored answer.
If no suitable FAQ is found and an API key is configured, the backend asks the AI model.
The result is returned as JSON and displayed on the webpage.

## 8. Future enhancements

- Student login
- JWT authentication
- Admin dashboard
- PDF/document upload
- RAG-based answers
- Conversation history
- Quiz generation
- Study progress tracking
