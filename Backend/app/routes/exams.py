from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from ..schemas.exams import Exam, ExamCreate, ExamSearch, ExamSolution, ExamSolutionCreate
from ..utils.database import get_db
from ..utils.exams_service import ExamsService
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/", response_model=List[Exam])
async def get_exams(
    year: Optional[str] = Query(None, description="Filter by year"),
    subject: Optional[str] = Query(None, description="Filter by subject"),
    exam_type: Optional[str] = Query(None, description="Filter by exam type"),
    limit: int = Query(50, description="Maximum number of results"),
    skip: int = Query(0, description="Number of results to skip"),
    db: Session = Depends(get_db)
):
    """Get all exam papers with optional filtering"""
    try:
        exams_service = ExamsService(db)
        exams = exams_service.get_exams(
            year=year,
            subject=subject,
            exam_type=exam_type,
            limit=limit,
            skip=skip
        )
        return exams
    except Exception as e:
        logger.error(f"Error fetching exams: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch exams")

@router.get("/{exam_id}", response_model=Exam)
async def get_exam(exam_id: int, db: Session = Depends(get_db)):
    """Get a specific exam by ID"""
    try:
        exams_service = ExamsService(db)
        exam = exams_service.get_exam_by_id(exam_id)
        if not exam:
            raise HTTPException(status_code=404, detail="Exam not found")
        return exam
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching exam {exam_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch exam")

@router.post("/", response_model=Exam)
async def create_exam(exam: ExamCreate, db: Session = Depends(get_db)):
    """Create a new exam paper"""
    try:
        exams_service = ExamsService(db)
        created_exam = exams_service.create_exam(exam)
        return created_exam
    except Exception as e:
        logger.error(f"Error creating exam: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create exam")

@router.put("/{exam_id}", response_model=Exam)
async def update_exam(exam_id: int, exam: ExamCreate, db: Session = Depends(get_db)):
    """Update an existing exam paper"""
    try:
        exams_service = ExamsService(db)
        updated_exam = exams_service.update_exam(exam_id, exam)
        if not updated_exam:
            raise HTTPException(status_code=404, detail="Exam not found")
        return updated_exam
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating exam {exam_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update exam")

@router.delete("/{exam_id}")
async def delete_exam(exam_id: int, db: Session = Depends(get_db)):
    """Delete an exam paper"""
    try:
        exams_service = ExamsService(db)
        success = exams_service.delete_exam(exam_id)
        if not success:
            raise HTTPException(status_code=404, detail="Exam not found")
        return {"message": "Exam deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting exam {exam_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete exam")

@router.get("/search/", response_model=List[Exam])
async def search_exams(
    query: Optional[str] = Query(None, description="Search query"),
    year: Optional[str] = Query(None, description="Filter by year"),
    subject: Optional[str] = Query(None, description="Filter by subject"),
    exam_type: Optional[str] = Query(None, description="Filter by exam type"),
    limit: int = Query(10, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """Search exam papers"""
    try:
        exams_service = ExamsService(db)
        search_params = ExamSearch(
            query=query,
            year=year,
            subject=subject,
            exam_type=exam_type,
            limit=limit
        )
        results = exams_service.search_exams(search_params)
        return results
    except Exception as e:
        logger.error(f"Error searching exams: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to search exams")

@router.get("/years/")
async def get_available_years(db: Session = Depends(get_db)):
    """Get all available exam years"""
    try:
        exams_service = ExamsService(db)
        years = exams_service.get_available_years()
        return {"years": years}
    except Exception as e:
        logger.error(f"Error fetching available years: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch available years")

@router.get("/subjects/")
async def get_available_subjects(db: Session = Depends(get_db)):
    """Get all available subjects"""
    try:
        exams_service = ExamsService(db)
        subjects = exams_service.get_available_subjects()
        return {"subjects": subjects}
    except Exception as e:
        logger.error(f"Error fetching available subjects: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch available subjects")

@router.get("/{exam_id}/solution")
async def get_exam_solution(exam_id: int, db: Session = Depends(get_db)):
    """Get solution for a specific exam"""
    try:
        exams_service = ExamsService(db)
        solution = exams_service.get_exam_solution(exam_id)
        if not solution:
            raise HTTPException(status_code=404, detail="Solution not found")
        return solution
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching solution for exam {exam_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch solution")

@router.post("/{exam_id}/solution")
async def create_exam_solution(
    exam_id: int, 
    solution: ExamSolutionCreate, 
    db: Session = Depends(get_db)
):
    """Create a solution for an exam"""
    try:
        exams_service = ExamsService(db)
        solution.exam_id = exam_id
        created_solution = exams_service.create_exam_solution(solution)
        return created_solution
    except Exception as e:
        logger.error(f"Error creating solution: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create solution")

@router.get("/statistics/")
async def get_exam_statistics(db: Session = Depends(get_db)):
    """Get exam statistics"""
    try:
        exams_service = ExamsService(db)
        stats = exams_service.get_exam_statistics()
        return stats
    except Exception as e:
        logger.error(f"Error fetching exam statistics: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch exam statistics") 