# 🎓 EUEE Study Companion: AI-Powered Learning Platform for Ethiopian High School Students

> A student-centric platform that provides structured access to curriculum-based learning resources and past national exam papers, designed to improve the EUEE pass rate through focused, accessible, and AI-enhanced revision tools.

---

## 📌 Purpose

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

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/euee-study-companion.git
cd euee-study-companion
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd Backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp ../env.example .env
# Edit .env with your configuration

# Initialize database
python -m alembic upgrade head

# Start the backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend Setup
```bash
# Navigate to frontend directory
cd Frontend

# Install dependencies
npm install

# Set up environment variables
cp ../env.example .env.local
# Edit .env.local with your configuration

# Start the development server
npm run dev
```

### 4. Database Setup
```bash
# Create PostgreSQL database
createdb euee_study_companion

# Run database migrations
cd Backend
alembic upgrade head
```

### 5. Process Documents (Optional)
```bash
# Process study materials for AI chatbot
cd Scripts
python process_documents.py --materials-dir ../Data/books --init-db
```

---

## 📂 Repository Structure

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
├── Frontend/                   # Next.js web interface (user journey)
│   ├── pages/                  # Page-level components (Home, Library, Exams, Chat)
│   ├── components/             # Reusable UI elements (Navbar, Card, Modal)
│   ├── services/               # API clients & data-fetching hooks
│   └── public/                 # Static assets (images, fonts, icons)
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
├── README.md                   # You are here: overview, setup, and contribution guide
└── LICENSE                     # MIT License
```

---

## 🔧 Configuration

### Environment Variables
Copy `env.example` to `.env` and configure:

**Backend (.env):**
```bash
DATABASE_URL=postgresql://user:password@localhost/euee_study_companion
OPENAI_API_KEY=your-openai-api-key
SUPABASE_URL=your-supabase-url
SUPABASE_ANON_KEY=your-supabase-anon-key
```

**Frontend (.env.local):**
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 🧪 Development

### Running Tests
```bash
# Backend tests
cd Backend
pytest

# Frontend tests
cd Frontend
npm test
```

### Code Quality
```bash
# Backend linting
cd Backend
black app/
isort app/
flake8 app/

# Frontend linting
cd Frontend
npm run lint
```

---

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🆘 Support

For support, email miftahh.dev@gmail.com or create an issue in this repository.

