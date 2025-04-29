# bard


A simple, scalable **chatbot backend service** built with **Python** (FastAPI), designed to handle user conversations with memory, authentication, and extensibility toward intelligent dialogue systems.

---

## ✨ Who

This project is created to **build a clean and extendable chatbot service**, including:

- Sending user messages to a chatbot engine
- Managing conversation sessions
- Retrieving chat history
- Clearing chat sessions
- Securing APIs with JWT authentication (integrated with an Auth Service)

Built with microservices architecture in mind.

---

## ⚙️ Tech Stack

- **Python** (FastAPI)
- **Redis** (for session and context management)
- **PostgreSQL** (for storing chat history)
- **JWT** (for user authentication)
- **Docker** (for containerization)
- **Optional:** Huggingface Transformers, OpenAI API, or custom NLU/NLG models

---

## 🚀 API Endpoints

| Endpoint               | Method | Purpose                                           |
| :--------------------- | :----- | :------------------------------------------------ |
| `/api/v1/chat/chat`    | POST   | Send a message to the chatbot and receive a reply |
| `/api/v1/chat/history` | GET    | Retrieve conversation history by session          |
| `/api/v1/chat/clear`   | POST   | Clear conversation memory by session              |
| `/api/v1/chat/status`  | GET    | Check chatbot online status                       |

> ⚡ **All endpoints (except `/status`) require JWT Authorization.**

---

## 🛠 Setup & Run

### 1. Clone the repository

```bash
git clone https://github.com/8Opt/bard.git
cd bard
```

### 2. Set up environment variables

Create a `.env` file in the project root:

```bash
REDIS_URL=redis://localhost:6379/0
POSTGRES_URL=postgresql://username:password@localhost:5432/chatbotdb
JWT_SECRET=your_jwt_secret_key
MODEL_PROVIDER=openai # or huggingface / local
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Run Redis and PostgreSQL locally (optional via Docker)

```bash
docker run --name chatbot-redis -p 6379:6379 -d redis
docker run --name chatbot-postgres -e POSTGRES_PASSWORD=password -e POSTGRES_USER=username -e POSTGRES_DB=chatbotdb -p 5432:5432 -d postgres
```

### 4. Install Python dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 5. Run the application

```bash
uvicorn main:app --reload --port 8000
```

Service will be available at:  
```http
http://localhost:8000
```

---

## 🧩 Project Structure

```bash
chatbot-service/
├── main.py
├── routers/
│   ├── chat.py
│   └── status.py
├── services/
│   ├── chatbot_engine.py
│   └── memory_manager.py
├── models/
│   ├── chat_request.py
│   └── chat_response.py
├── utils/
│   └── token_validator.py
├── config/
│   └── settings.py
├── database/
│   ├── redis_session.py
│   └── postgres_history.py
├── requirements.txt
└── README.md
```

---

## 🔒 Security Features

- Every user request is **authenticated via JWT**.
- Only authorized users can send messages or retrieve history.
- Access tokens are verified on every API call.

---

## 🧠 Future Enhancements

- Streaming chat responses (WebSocket support)
- Retrieval-Augmented Generation (RAG) using Vector DB
- User feedback collection (thumbs up/down per response)
- Admin dashboard for conversation analytics
- Multi-language support (dynamic translation)
- Integration with Human-in-the-loop (escalation to human agent)

---

## 📄 License

This project is open-source under the [MIT License](LICENSE).

---
