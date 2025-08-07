# 🎓 EUEE Study Companion: AI-Powered Learning Platform for Ethiopian High School Students

> A student-centric platform that provides structured access to curriculum-based learning resources and past national exam papers, designed to improve the EUEE pass rate through focused, accessible, and AI-enhanced revision tools.

---
 📌 Purpose

Only **2–5%** of Ethiopian students successfully pass the **Ethiopian University Entrance Exam (EUEE)**. This project exists to **solve that problem** by offering:
- ✅ Centralized access to **Grade 9–12 textbooks and reference materials**
- ✅ Categorized **EUEE past 10-year exam papers**
- ✅ A clean, searchable, and user-friendly interface
- ✅ Future potential to scale into a fully AI-supported learning system

---

## 🚀 Key Features
| Feature                         | Description                                                                                     |
|---------------------------------|-------------------------------------------------------------------------------------------------|
| 📚 Pre-Uploaded Materials       | Organized textbooks and references from Grade 9 to 12, just like a personal library             |
| 📄 Previous Years EUEE Past Papers | Filterable by year and subject                                                                |
| 🔍 Clean Study Interface        | Distraction-free material viewer                                                               |
| 📦 Modular & Extensible Design  | Codebase structured for easy feature extension                                                 |
| 💡 Future Roadmap-Ready         | Built with tools aligned to LangChain, n8n, and automation ecosystems                           |
| ✅ Custom Material Upload       | Allows students to upload and read their own study files (PDFs, text) for personalized learning |
| 🤖 AI Chatbot for Custom Books | Students can chat with an AI tutor powered by their own uploaded study materials                 |

## 🛠️ Tech Stack

| Layer              | Tool Used         | Reason Chosen                                                              |
|--------------------|------------------|----------------------------------------------------------------------------|
| Backend            | **FastAPI**       | Lightweight, async-ready API framework ideal for modular AI apps          |
| Frontend           | **Next.js**       | Fast, SEO-friendly React framework with great developer experience        |
| Data Storage       | **Supabase**      | PostgreSQL + built-in Auth and File Storage (fully roadmap-aligned)       |
| Deployment         | **Railway**       | Easy CI/CD + instant backend/frontend deploys                             |
| Version Control    | **GitHub**        | Central collaboration and open-source visibility                          |

👥 Team:
•	Mifta Yibrahim (Team Lead) – miftahh.dev@gmail.com
•	Meheretabe Abayneh
•	Abdurahman Kero
•	Musab Gemil

 📂 Repository Structure

```bash
euee-study-companion/
├── Backend/                    # FastAPI REST API (core application logic)
│   ├── app/
│   │   ├── main.py             # Entry point: server startup & middleware
│   │   ├── routes/             # Route handlers (materials, exams, custom uploads, chatbot)
│   │   ├── schemas/            # Pydantic models for request/response validation
│   │   ├── models/             # SQLAlchemy database models
│   │   └── utils/              # Helpers: PDF parsing, file I/O, embedding functions
│   └── requirements.txt        # Backend Python dependencies
│
├── Frontend/                   # React.js SPA (client-side rendering)
│   ├── public/                 # Static assets
│   │   ├── index.html          # Main HTML entry
│   │   ├── images/             # App visuals
│   │   └── fonts/              # Custom typography
│   ├── src/
│   │   ├── components/         # Reusable UI (Navbar.jsx, Card.jsx, Modal.jsx)
│   │   ├── pages/              # Route components (Home.jsx, Library.jsx, Exams.jsx, Chat.jsx)
│   │   ├── services/           # API clients (axios config, fetch hooks)
│   │   └── App.jsx            # Router setup (react-router-dom)
│   └── package.json           # Includes react-router-dom
│
├── Data/                       # Core study materials & vectors
│   ├── books/                  # Grade 9–12 PDFs & extracted text files
│   └── exams/                  # Past 10-year EUEE exam PDFs & metadata
│
├── Scripts/                    # Automation & build scripts
│   └── process_documents.py    # Script to parse, chunk & index documents into FAISS
│
├── Supabase/                   # Supabase setup: SQL schema, auth rules & storage policies
│
├── Docs/                       # Design docs, architecture diagrams, screenshots
│
├── env.example                 # Template for environment variables
├── README.md                   # Project overview and setup guide
└── LICENSE                     # MIT License
```

-## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


## 🆘 Support

For support, email miftahh.dev@gmail.com or create an issue in this repository.

