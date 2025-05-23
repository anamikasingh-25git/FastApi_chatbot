# FastAPI Chat Backend with Branching Functionality

## 🚀 Overview

This is a **microservice-based chat backend** built with **FastAPI**, designed to support branching chat conversations. The system allows users to:

* Create and manage chat conversations
* Add messages and responses
* Branch from any point in the conversation
* Store metadata in PostgreSQL and content in MongoDB

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/fastapi-chat-backend.git
cd fastapi-chat-backend
```
---

##  🚀 Start Dockerized Databases
From the root of your project, run:

```bash
docker-compose up -d
```
This will start:

PostgreSQL for chat metadata

MongoDB for storing dynamic conversation content

---
### 2. Create and Activate Virtual Environment

```bash
python3 -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file and include the following:

```
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/chatdb
MONGO_URL=mongodb://localhost:27017/
SECRET_KEY=your_secret_key
```

## 🔄 Database Migration Scripts

### 1. Initialize Alembic (already done)

```bash
alembic init alembic
```

### 2. Generate a Migration Script

```bash
alembic revision --autogenerate -m "Add chat and conversation models"
```

### 3. Apply Migrations

```bash
alembic upgrade head
```

If you'd like the exact contents of a sample migration file or Docker support added, let me know!

---

### 6. Run the Server

```bash
uvicorn main:app --reload
```

---

## 🔌 API Documentation

### Authentication

* `POST /api/v1/auth/register` — Register a new user
* `POST /api/v1/auth/login` — Authenticate and get token

### Chat Management

* `POST /api/v1/chats/create-chat` — Create a chat
* `GET /api/v1/chats/get-chat` — Get all user chats
* `PUT /api/v1/chats/update-chat/{chat_id}` — Update chat
* `DELETE /api/v1/chats/delete-chat/{chat_id}` — Delete chat

### Message Management

* `POST /api/v1/messages/add-message` — Add message to chat

### Branch Management

* `POST /api/v1/branches/create-branch` — Create a branch from a response
* `GET /api/v1/branches/get-branches?chat_id=uuid` — Get branches for a chat
* `PUT /api/v1/branches/set-active-branch` — Mark a branch as active

### Conversation Management

* `POST /api/v1/conversations/` — Add a conversation record

## 🧠 Design Decisions

* **FastAPI**: Chosen for its speed, modern features, and async support.
* **PostgreSQL**: Used for structured data like users, chats, and metadata.
* **MongoDB**: Perfect fit for flexible QA pair storage with embedded branches.
* **Alembic**: Used for versioned migrations on PostgreSQL.
* **Motor**: Async driver for MongoDB to enable non-blocking I/O.
* **Modular Structure**: Separation of concerns into routers, models, services, and schemas.
