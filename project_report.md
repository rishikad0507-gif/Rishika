# AI FAQ Assistant API – Project Report

## Title
AI-Augmented Backend Development – AI FAQ Assistant API

## Abstract
The AI FAQ Assistant is a simple backend application that helps students get answers to frequently asked questions. The system stores FAQs in an SQLite database and exposes REST API endpoints using FastAPI. When a matching FAQ is not available, an optional AI service can generate a short answer.

## Objectives
1. Build a REST API using Python FastAPI.
2. Store FAQ information in a database.
3. Allow users to ask questions.
4. Provide an AI fallback for unknown questions.
5. Demonstrate CRUD operations and API testing.

## Modules
### 1. FAQ Management
Add, view and delete FAQs.

### 2. Question Answering
The user sends a question to `/api/ask`.

### 3. Database
SQLite stores question, answer and category.

### 4. AI Integration
The OpenAI API is optionally used when a local FAQ does not match.

### 5. Frontend
A simple HTML page communicates with the backend using JavaScript fetch requests.

## System Flow

User
  ↓
Web Interface
  ↓
FastAPI Backend
  ↓
FAQ Database
  ↓
Matching FAQ?
  ├── Yes → Return FAQ answer
  └── No → Optional AI → Return answer

## Conclusion
The project demonstrates how AI can be added to a backend API without making the application complicated. It is suitable as a beginner/intermediate backend project and can later be extended with authentication, RAG, document uploads and analytics.
