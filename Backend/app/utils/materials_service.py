from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from ..schemas.materials import MaterialCreate, MaterialSearch, ChapterCreate
from ..models.materials import Material, Chapter
import logging

logger = logging.getLogger(__name__)

class MaterialsService:
    def __init__(self, db: Session):
        self.db = db

    def get_materials(
        self,
        subject: Optional[str] = None,
        grade_level: Optional[str] = None,
        limit: int = 50,
        skip: int = 0
    ) -> List[Material]:
        """Get materials with optional filtering"""
        query = self.db.query(Material)
        
        if subject:
            query = query.filter(Material.subject == subject)
        if grade_level:
            query = query.filter(Material.grade_level == grade_level)
        
        return query.offset(skip).limit(limit).all()

    def get_material_by_id(self, material_id: int) -> Optional[Material]:
        """Get material by ID"""
        return self.db.query(Material).filter(Material.id == material_id).first()

    def create_material(self, material: MaterialCreate) -> Material:
        """Create a new material"""
        db_material = Material(**material.dict())
        self.db.add(db_material)
        self.db.commit()
        self.db.refresh(db_material)
        return db_material

    def update_material(self, material_id: int, material: MaterialCreate) -> Optional[Material]:
        """Update an existing material"""
        db_material = self.get_material_by_id(material_id)
        if not db_material:
            return None
        
        for key, value in material.dict().items():
            setattr(db_material, key, value)
        
        self.db.commit()
        self.db.refresh(db_material)
        return db_material

    def delete_material(self, material_id: int) -> bool:
        """Delete a material"""
        db_material = self.get_material_by_id(material_id)
        if not db_material:
            return False
        
        self.db.delete(db_material)
        self.db.commit()
        return True

    def search_materials(self, search_params: MaterialSearch) -> List[Material]:
        """Search materials"""
        query = self.db.query(Material)
        
        # Basic text search
        if search_params.query:
            search_term = f"%{search_params.query}%"
            query = query.filter(
                or_(
                    Material.title.ilike(search_term),
                    Material.description.ilike(search_term)
                )
            )
        
        # Apply filters
        if search_params.subject:
            query = query.filter(Material.subject == search_params.subject)
        if search_params.grade_level:
            query = query.filter(Material.grade_level == search_params.grade_level)
        
        return query.limit(search_params.limit).all()

    def get_material_chapters(self, material_id: int) -> List[Chapter]:
        """Get chapters for a material"""
        return self.db.query(Chapter).filter(Chapter.material_id == material_id).all()

    def create_chapter(self, chapter: ChapterCreate) -> Chapter:
        """Create a new chapter"""
        db_chapter = Chapter(**chapter.dict())
        self.db.add(db_chapter)
        self.db.commit()
        self.db.refresh(db_chapter)
        return db_chapter

    def get_materials_by_subject(self, subject: str) -> List[Material]:
        """Get all materials for a specific subject"""
        return self.db.query(Material).filter(Material.subject == subject).all()

    def get_materials_by_grade(self, grade_level: str) -> List[Material]:
        """Get all materials for a specific grade level"""
        return self.db.query(Material).filter(Material.grade_level == grade_level).all()

    def get_material_statistics(self) -> dict:
        """Get material statistics"""
        total_materials = self.db.query(Material).count()
        
        # Count by subject
        subject_counts = {}
        subjects = self.db.query(Material.subject).distinct().all()
        for subject in subjects:
            count = self.db.query(Material).filter(Material.subject == subject[0]).count()
            subject_counts[subject[0]] = count
        
        # Count by grade level
        grade_counts = {}
        grades = self.db.query(Material.grade_level).distinct().all()
        for grade in grades:
            count = self.db.query(Material).filter(Material.grade_level == grade[0]).count()
            grade_counts[grade[0]] = count
        
        return {
            "total_materials": total_materials,
            "by_subject": subject_counts,
            "by_grade": grade_counts
        } 