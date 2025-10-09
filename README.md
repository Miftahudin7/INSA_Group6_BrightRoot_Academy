

# 🌱 BrightRoot Academy Platform

**BrightRoot Academy** is an **AI-powered learning platform** that blends an interactive frontend, a secure backend, and  AI-driven services to deliver a **modern, personalized education experience** for students and instructors.

---

## 🚀 Features

### 🎨 Frontend (React + TailwindCSS)

* Fully responsive, dark-mode enabled interface
* Dynamic student and instructor dashboards
* Seamless course discovery and signup flow

### ⚙️ Backend (Django REST Framework)

* Secure authentication and user role management (Admin / Instructor / Student)
* Course, enrollment, and progress tracking APIs
* RESTful endpoints with JWT authentication

### 🤖 AI Layer

* **RAG-powered chatbot** for course-specific Q&A
* **Personalized learning recommendations** using embeddings
* **Vector database (pgvector / Supabase)** for intelligent retrieval

---

## 🧩 Tech Stack

| Layer              | Technologies                                  |
| :----------------- | :-------------------------------------------- |
| **Frontend**       | React, TailwindCSS, Vite                      |
| **Backend**        | Django REST Framework, PostgreSQL             |
| **AI / LLM**       | OpenAI API, RAG, pgvector (Supabase)          |
| **Infra / DevOps** | Docker, Render/Heroku, GitHub Actions (CI/CD) |

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/Miftahudin7/brightroot-academy.git
cd brightroot-academy
```

### 2️⃣ Backend Setup

```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 3️⃣ Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

---

## 📂 Project Structure

```
brightroot-academy/
│
├── backend/                # Django REST API
│   ├── manage.py
│   ├── requirements.txt
│   ├── apps/
│   └── ...
│
├── frontend/               # React + Vite frontend
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── context/
│   │   ├── services/
│   │   └── styles/
│   ├── App.jsx
│   ├── index.html
│   └── vite.config.js
│
└── README.md
```

---

## 🎯 Roadmap

* 🧠 Expand AI tutoring workflows (multi-agent feedback + grading)
* ☁️ Full Docker deployment to Render / AWS
* 📊 Instructor analytics dashboard
* 🧩 Real-time chat and video learning features

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a new branch (`feature/your-feature-name`)
3. Commit your changes and open a pull request

---

## 📜 License

**MIT License** © 2025 [BrightRoot Academy](https://github.com/Miftahudin7)
