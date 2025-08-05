from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from ..schemas.materials import Material, MaterialCreate, MaterialSearch, Chapter, ChapterCreate
from ..utils.database import get_db
from ..utils.materials_service import MaterialsService
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/", response_model=List[Material])
async def get_materials(
    subject: Optional[str] = Query(None, description="Filter by subject"),
    grade_level: Optional[str] = Query(None, description="Filter by grade level"),
    limit: int = Query(50, description="Maximum number of results"),
    skip: int = Query(0, description="Number of results to skip"),
    db: Session = Depends(get_db)
):
    """Get all study materials with optional filtering"""
    try:
        materials_service = MaterialsService(db)
        materials = materials_service.get_materials(
            subject=subject,
            grade_level=grade_level,
            limit=limit,
            skip=skip
        )
        return materials
    except Exception as e:
        logger.error(f"Error fetching materials: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch materials")

@router.get("/{material_id}", response_model=Material)
async def get_material(material_id: int, db: Session = Depends(get_db)):
    """Get a specific study material by ID"""
    try:
        materials_service = MaterialsService(db)
        material = materials_service.get_material_by_id(material_id)
        if not material:
            raise HTTPException(status_code=404, detail="Material not found")
        return material
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching material {material_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch material")

@router.post("/", response_model=Material)
async def create_material(material: MaterialCreate, db: Session = Depends(get_db)):
    """Create a new study material"""
    try:
        materials_service = MaterialsService(db)
        created_material = materials_service.create_material(material)
        return created_material
    except Exception as e:
        logger.error(f"Error creating material: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create material")

@router.put("/{material_id}", response_model=Material)
async def update_material(material_id: int, material: MaterialCreate, db: Session = Depends(get_db)):
    """Update an existing study material"""
    try:
        materials_service = MaterialsService(db)
        updated_material = materials_service.update_material(material_id, material)
        if not updated_material:
            raise HTTPException(status_code=404, detail="Material not found")
        return updated_material
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating material {material_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update material")

@router.delete("/{material_id}")
async def delete_material(material_id: int, db: Session = Depends(get_db)):
    """Delete a study material"""
    try:
        materials_service = MaterialsService(db)
        success = materials_service.delete_material(material_id)
        if not success:
            raise HTTPException(status_code=404, detail="Material not found")
        return {"message": "Material deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting material {material_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete material")

@router.get("/search/", response_model=List[Material])
async def search_materials(
    query: str = Query(..., description="Search query"),
    subject: Optional[str] = Query(None, description="Filter by subject"),
    grade_level: Optional[str] = Query(None, description="Filter by grade level"),
    limit: int = Query(10, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """Search study materials"""
    try:
        materials_service = MaterialsService(db)
        search_params = MaterialSearch(
            query=query,
            subject=subject,
            grade_level=grade_level,
            limit=limit
        )
        results = materials_service.search_materials(search_params)
        return results
    except Exception as e:
        logger.error(f"Error searching materials: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to search materials")

@router.get("/{material_id}/chapters", response_model=List[Chapter])
async def get_material_chapters(material_id: int, db: Session = Depends(get_db)):
    """Get chapters for a specific material"""
    try:
        materials_service = MaterialsService(db)
        chapters = materials_service.get_material_chapters(material_id)
        return chapters
    except Exception as e:
        logger.error(f"Error fetching chapters for material {material_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch chapters")

@router.post("/{material_id}/chapters", response_model=Chapter)
async def create_chapter(
    material_id: int, 
    chapter: ChapterCreate, 
    db: Session = Depends(get_db)
):
    """Create a new chapter for a material"""
    try:
        materials_service = MaterialsService(db)
        chapter.material_id = material_id
        created_chapter = materials_service.create_chapter(chapter)
        return created_chapter
    except Exception as e:
        logger.error(f"Error creating chapter: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create chapter") 