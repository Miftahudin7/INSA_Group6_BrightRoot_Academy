
# BrightRoot Academy Platform

An AI-powered **Learning Management System (LMS)** designed for BrightRoot Academy. The platform integrates **interactive frontend, secure backend, and intelligent AI services** to deliver a modern, personalized education experience.

---

## 🚀 Features

* **Frontend (React + Tailwind)**:

  * Responsive, dark mode UI
  * Student & instructor dashboards
  * Course browsing 

* **Backend (Django REST API)**:

  * Authentication & user roles (students/instructors/admins)
  * Course, enrollment & progress management
  * Secure API endpoints

* **AI Layer (LangChain + Groq)**:

  * RAG-powered chatbot for course Q\&A
  * Personalized learning recommendations
  * Vector database integration for knowledge retrieval

---

## 🛠 Tech Stack

* **Frontend**: React, TailwindCSS, Vite
* **Backend**: Django REST Framework, PostgreSQL
* **AI/LLM**: LangChain, Groq, ChromaDB (vector DB)
* **Infra/DevOps**: Docker, GitHub Actions (CI/CD), Render/Heroku

---

## ⚙️ Installation

1. **Clone repo**

```bash
git clone https://github.com/your-username/brightroot-academy.git
cd brightroot-academy
```

2. **Setup Backend**

```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

3. **Setup Frontend**

```bash
cd frontend
npm install
npm run dev
```

---

## 📂 Project Structure

```
brightroot/
├── backend/
│   ├── manage.py
│   ├── brightroot/                # settings, urls, wsgi/asgi
│   ├── api/                       # DRF viewsets, serializers, routers
│   │   ├── auth/                  # register/login endpoints
│   │   ├── files/                 # upload/list/download endpoints
│   │   ├── ai/                    # summarize/quiz endpoints (Gemini)
│   │   └── common/                # utils, pagination, permissions
│   ├── core/                      # Django models (User, Streak, AI logs, etc.)
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── auth/              # Login/Register (Context API)
    │   │   ├── pages/             # Dashboard, Uploads, AI tools
    │   │   └── ui/                # Reusable UI
    │   ├── services/              # axios clients
    │   ├── context/               # Auth + Theme context
    │   ├── styles/                # Dark theme tokens
    │   └── main.tsx
    └── Read.me


```

---

## 🎯 Roadmap

* ✅ MVP with core LMS features
* ✅ AI-powered Q\&A chatbot
* 🔄 Multi-agent workflows (tutoring, grading, feedback)
* 🔄 Deployment to cloud (Docker + Render)

---

## 🤝 Contributing

We welcome contributions! Please fork the repo, create a branch, and submit a PR.

---

## 📜 License

MIT License © 2025 BrightRoot Academy
