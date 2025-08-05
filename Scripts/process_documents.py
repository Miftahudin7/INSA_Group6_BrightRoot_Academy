#!/usr/bin/env python3
"""
Document Processing Script for EUEE Study Companion

This script processes uploaded documents (PDFs, DOCX, TXT) and creates embeddings
for the AI chatbot functionality. It extracts text, chunks it, and stores embeddings
in a vector database for semantic search.
"""

import os
import sys
import logging
from pathlib import Path
from typing import List, Dict, Any
import argparse

# Add the backend directory to the Python path
sys.path.append(str(Path(__file__).parent.parent / "Backend"))

from app.utils.file_processor import FileProcessor
from app.utils.embedding_service import EmbeddingService
from app.utils.database import SessionLocal, init_db
from app.models.materials import Material
from app.models.uploads import UserUpload

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DocumentProcessor:
    def __init__(self):
        self.file_processor = FileProcessor()
        self.embedding_service = EmbeddingService()
        self.db = SessionLocal()

    def process_materials_directory(self, materials_dir: str) -> None:
        """Process all materials in the specified directory"""
        materials_path = Path(materials_dir)
        
        if not materials_path.exists():
            logger.error(f"Materials directory {materials_dir} does not exist")
            return

        logger.info(f"Processing materials in {materials_dir}")
        
        for file_path in materials_path.rglob("*"):
            if file_path.is_file() and self.file_processor.is_supported_file_type(file_path.name):
                try:
                    self.process_single_file(file_path)
                except Exception as e:
                    logger.error(f"Error processing {file_path}: {str(e)}")

    def process_single_file(self, file_path: Path) -> None:
        """Process a single file and create embeddings"""
        logger.info(f"Processing {file_path}")
        
        # Extract text from file
        text_content = self.file_processor.extract_text(file_path)
        
        if not text_content:
            logger.warning(f"No text content extracted from {file_path}")
            return

        # Split text into chunks
        chunks = self.file_processor.split_text_into_chunks(text_content)
        
        # Create embeddings for chunks
        embeddings = self.embedding_service.create_embeddings(chunks)
        
        # Store embeddings in vector database
        self.embedding_service.store_embeddings(
            file_path.name,
            chunks,
            embeddings,
            metadata={
                "file_path": str(file_path),
                "file_type": file_path.suffix,
                "file_size": file_path.stat().st_size
            }
        )
        
        logger.info(f"Successfully processed {file_path} - {len(chunks)} chunks created")

    def process_uploaded_files(self) -> None:
        """Process all uploaded files in the database"""
        logger.info("Processing uploaded files from database")
        
        uploads = self.db.query(UserUpload).filter(
            UserUpload.status == "completed",
            UserUpload.embedding_ready == False
        ).all()
        
        for upload in uploads:
            try:
                file_path = Path(upload.file_path)
                if file_path.exists():
                    self.process_single_file(file_path)
                    upload.embedding_ready = True
                    self.db.commit()
                    logger.info(f"Updated embedding status for upload {upload.id}")
                else:
                    logger.warning(f"File not found for upload {upload.id}: {upload.file_path}")
            except Exception as e:
                logger.error(f"Error processing upload {upload.id}: {str(e)}")

    def create_material_embeddings(self) -> None:
        """Create embeddings for all materials in the database"""
        logger.info("Creating embeddings for materials")
        
        materials = self.db.query(Material).all()
        
        for material in materials:
            try:
                file_path = Path(material.file_path)
                if file_path.exists():
                    self.process_single_file(file_path)
                    logger.info(f"Created embeddings for material {material.id}")
                else:
                    logger.warning(f"File not found for material {material.id}: {material.file_path}")
            except Exception as e:
                logger.error(f"Error processing material {material.id}: {str(e)}")

    def cleanup_old_embeddings(self, days_old: int = 30) -> None:
        """Clean up old embeddings"""
        logger.info(f"Cleaning up embeddings older than {days_old} days")
        self.embedding_service.cleanup_old_embeddings(days_old)

    def get_statistics(self) -> Dict[str, Any]:
        """Get processing statistics"""
        stats = {
            "total_materials": self.db.query(Material).count(),
            "total_uploads": self.db.query(UserUpload).count(),
            "processed_uploads": self.db.query(UserUpload).filter(
                UserUpload.embedding_ready == True
            ).count(),
            "embedding_index_size": self.embedding_service.get_index_size()
        }
        return stats

def main():
    parser = argparse.ArgumentParser(description="Process documents for EUEE Study Companion")
    parser.add_argument("--materials-dir", help="Directory containing study materials")
    parser.add_argument("--uploaded-files", action="store_true", help="Process uploaded files")
    parser.add_argument("--materials", action="store_true", help="Process materials from database")
    parser.add_argument("--cleanup", type=int, metavar="DAYS", help="Clean up old embeddings")
    parser.add_argument("--stats", action="store_true", help="Show processing statistics")
    parser.add_argument("--init-db", action="store_true", help="Initialize database tables")

    args = parser.parse_args()

    if args.init_db:
        logger.info("Initializing database tables")
        init_db()
        return

    processor = DocumentProcessor()

    if args.materials_dir:
        processor.process_materials_directory(args.materials_dir)

    if args.uploaded_files:
        processor.process_uploaded_files()

    if args.materials:
        processor.create_material_embeddings()

    if args.cleanup:
        processor.cleanup_old_embeddings(args.cleanup)

    if args.stats:
        stats = processor.get_statistics()
        logger.info("Processing Statistics:")
        for key, value in stats.items():
            logger.info(f"  {key}: {value}")

    if not any([args.materials_dir, args.uploaded_files, args.materials, args.cleanup, args.stats, args.init_db]):
        parser.print_help()

if __name__ == "__main__":
    main() 