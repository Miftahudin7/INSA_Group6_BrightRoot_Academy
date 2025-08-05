from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from typing import List, Optional
from sqlalchemy.orm import Session
from ..schemas.uploads import UserUpload, UserUploadCreate, UploadResponse, FileUploadRequest, UploadSearch
from ..utils.database import get_db
from ..utils.uploads_service import UploadsService
from ..utils.file_processor import FileProcessor
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/file", response_model=UploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    title: str = Form(...),
    description: Optional[str] = Form(None),
    tags: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """Upload a study file"""
    try:
        uploads_service = UploadsService(db)
        file_processor = FileProcessor()
        
        # Validate file type
        if not file_processor.is_supported_file_type(file.filename):
            raise HTTPException(status_code=400, detail="Unsupported file type")
        
        # Process tags
        tag_list = []
        if tags:
            tag_list = [tag.strip() for tag in tags.split(",")]
        
        # Create upload record
        upload_data = UserUploadCreate(
            title=title,
            description=description,
            file_path="",  # Will be set by service
            file_size=0,   # Will be set by service
            file_type=file_processor.get_file_type(file.filename),
            original_filename=file.filename,
            user_id=None  # TODO: Get from auth
        )
        
        upload = uploads_service.create_upload(upload_data, file)
        return UploadResponse(
            upload_id=upload.id,
            message="File uploaded successfully",
            file_url=f"/uploads/{upload.file_path}",
            processing_status=upload.status
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to upload file")

@router.get("/", response_model=List[UserUpload])
async def get_uploads(
    user_id: Optional[int] = None,
    file_type: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 50,
    skip: int = 0,
    db: Session = Depends(get_db)
):
    """Get user uploads with optional filtering"""
    try:
        uploads_service = UploadsService(db)
        uploads = uploads_service.get_uploads(
            user_id=user_id,
            file_type=file_type,
            status=status,
            limit=limit,
            skip=skip
        )
        return uploads
    except Exception as e:
        logger.error(f"Error fetching uploads: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch uploads")

@router.get("/{upload_id}", response_model=UserUpload)
async def get_upload(upload_id: int, db: Session = Depends(get_db)):
    """Get a specific upload by ID"""
    try:
        uploads_service = UploadsService(db)
        upload = uploads_service.get_upload_by_id(upload_id)
        if not upload:
            raise HTTPException(status_code=404, detail="Upload not found")
        return upload
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching upload {upload_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch upload")

@router.delete("/{upload_id}")
async def delete_upload(upload_id: int, db: Session = Depends(get_db)):
    """Delete an upload"""
    try:
        uploads_service = UploadsService(db)
        success = uploads_service.delete_upload(upload_id)
        if not success:
            raise HTTPException(status_code=404, detail="Upload not found")
        return {"message": "Upload deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting upload {upload_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete upload")

@router.get("/search/", response_model=List[UserUpload])
async def search_uploads(
    query: Optional[str] = None,
    file_type: Optional[str] = None,
    status: Optional[str] = None,
    user_id: Optional[int] = None,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Search uploads"""
    try:
        uploads_service = UploadsService(db)
        search_params = UploadSearch(
            query=query,
            file_type=file_type,
            status=status,
            user_id=user_id,
            limit=limit
        )
        results = uploads_service.search_uploads(search_params)
        return results
    except Exception as e:
        logger.error(f"Error searching uploads: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to search uploads")

@router.post("/{upload_id}/process")
async def process_upload(upload_id: int, db: Session = Depends(get_db)):
    """Process an uploaded file (extract text, create embeddings)"""
    try:
        uploads_service = UploadsService(db)
        success = uploads_service.process_upload(upload_id)
        if not success:
            raise HTTPException(status_code=404, detail="Upload not found")
        return {"message": "Upload processing started"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing upload {upload_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to process upload")

@router.get("/{upload_id}/content")
async def get_upload_content(upload_id: int, db: Session = Depends(get_db)):
    """Get the processed content of an upload"""
    try:
        uploads_service = UploadsService(db)
        content = uploads_service.get_upload_content(upload_id)
        if not content:
            raise HTTPException(status_code=404, detail="Upload content not found")
        return {"content": content}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching upload content {upload_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch upload content")

@router.get("/statistics/")
async def get_upload_statistics(db: Session = Depends(get_db)):
    """Get upload statistics"""
    try:
        uploads_service = UploadsService(db)
        stats = uploads_service.get_upload_statistics()
        return stats
    except Exception as e:
        logger.error(f"Error fetching upload statistics: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch upload statistics") 