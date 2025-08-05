from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
from pathlib import Path
import os

# Import routes
from .routes import materials, exams, uploads, chatbot, auth

# Create FastAPI app instance
app = FastAPI(
    title="EUEE Study Companion API",
    description="AI-Powered Learning Platform for Ethiopian High School Students",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(materials.router, prefix="/api/materials", tags=["Study Materials"])
app.include_router(exams.router, prefix="/api/exams", tags=["Exam Papers"])
app.include_router(uploads.router, prefix="/api/uploads", tags=["File Uploads"])
app.include_router(chatbot.router, prefix="/api/chatbot", tags=["AI Chatbot"])

# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "EUEE Study Companion API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Mount static files for uploaded materials
uploads_dir = Path("uploads")
uploads_dir.mkdir(exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 