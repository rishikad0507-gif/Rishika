from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import sqlite3
import os

DB = "faq.db"

app = FastAPI(title="AI FAQ Assistant API", version="1.0.0")

class AskRequest(BaseModel):
    question: str

class FAQCreate(BaseModel):
    question: str
    answer: str
    category: str = "General"

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS faqs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            category TEXT NOT NULL
        )
    """)
    count = conn.execute("SELECT COUNT(*) AS c FROM faqs").fetchone()["c"]
    if count == 0:
        sample = [
            ("What is Python?", "Python is a simple, high-level programming language.", "Programming"),
            ("What is DBMS?", "DBMS is software used to create, store and manage databases.", "Database"),
            ("What is an API?", "An API allows different software applications to communicate with each other.", "Web"),
            ("What is FastAPI?", "FastAPI is a modern Python framework for building APIs.", "Programming"),
            ("What is AI?", "Artificial Intelligence is technology that enables computers to perform tasks that normally require human intelligence.", "AI"),
        ]
        conn.executemany(
            "INSERT INTO faqs(question, answer, category) VALUES (?, ?, ?)",
            sample
        )
    conn.commit()
    conn.close()

init_db()

@app.get("/")
def home():
    return FileResponse("static/index.html")

@app.get("/api/faqs")
def get_faqs():
    conn = get_db()
    rows = conn.execute("SELECT * FROM faqs ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.post("/api/faqs")
def add_faq(faq: FAQCreate):
    if not faq.question.strip() or not faq.answer.strip():
        raise HTTPException(status_code=400, detail="Question and answer are required")
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO faqs(question, answer, category) VALUES (?, ?, ?)",
        (faq.question.strip(), faq.answer.strip(), faq.category.strip() or "General")
    )
    conn.commit()
    row = conn.execute("SELECT * FROM faqs WHERE id = ?", (cur.lastrowid,)).fetchone()
    conn.close()
    return dict(row)

@app.delete("/api/faqs/{faq_id}")
def delete_faq(faq_id: int):
    conn = get_db()
    cur = conn.execute("DELETE FROM faqs WHERE id = ?", (faq_id,))
    conn.commit()
    conn.close()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="FAQ not found")
    return {"message": "FAQ deleted"}

@app.post("/api/ask")
def ask(req: AskRequest):
    question = req.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question is required")

    # First try the local FAQ database.
    conn = get_db()
    rows = conn.execute("SELECT * FROM faqs").fetchall()
    conn.close()

    q = question.lower()
    best = None
    best_score = 0
    for row in rows:
        words = set(row["question"].lower().split())
        score = sum(1 for word in q.split() if word in words and len(word) > 2)
        if score > best_score:
            best_score = score
            best = row

    if best and best_score >= 1:
        return {
            "answer": best["answer"],
            "source": "FAQ database",
            "category": best["category"]
        }

    # Optional AI fallback.
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            response = client.responses.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                input=(
                    "You are a helpful college FAQ assistant. "
                    "Answer briefly and clearly for a student. "
                    f"Question: {question}"
                )
            )
            return {
                "answer": response.output_text,
                "source": "AI",
                "category": "AI"
            }
        except Exception:
            pass

    return {
        "answer": "I could not find this in the FAQ database. Add the question and answer as a new FAQ, or configure OPENAI_API_KEY for AI answers.",
        "source": "Fallback",
        "category": "General"
    }

app.mount("/static", StaticFiles(directory="static"), name="static")
