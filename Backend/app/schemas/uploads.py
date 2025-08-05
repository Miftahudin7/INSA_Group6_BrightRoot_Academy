from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class FileType(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"
    IMAGE = "image"
    OTHER = "other"

class UploadStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class UserUploadBase(BaseModel):
    title: str = Field(..., description="Title of the uploaded material")
    description: Optional[str] = Field(None, description="Description of the material")
    file_path: str = Field(..., description="Path to the uploaded file")
    file_size: int = Field(..., description="File size in bytes")
    file_type: FileType = Field(..., description="Type of uploaded file")
    original_filename: str = Field(..., description="Original filename")
    user_id: Optional[int] = Field(None, description="ID of the user who uploaded")

class UserUploadCreate(UserUploadBase):
    pass

class UserUpload(UserUploadBase):
    id: int
    status: UploadStatus = Field(UploadStatus.PENDING, description="Processing status")
    created_at: datetime
    updated_at: datetime
    processed_content: Optional[str] = Field(None, description="Extracted text content")
    embedding_ready: bool = Field(False, description="Whether file is ready for embedding")
    
    class Config:
        from_attributes = True

class UploadResponse(BaseModel):
    upload_id: int
    message: str
    file_url: Optional[str] = Field(None, description="URL to access the uploaded file")
    processing_status: UploadStatus

class FileUploadRequest(BaseModel):
    title: str = Field(..., description="Title for the uploaded material")
    description: Optional[str] = Field(None, description="Description of the material")
    tags: Optional[List[str]] = Field(None, description="Tags for categorization")

class UploadSearch(BaseModel):
    query: Optional[str] = Field(None, description="Search query")
    file_type: Optional[FileType] = Field(None, description="Filter by file type")
    status: Optional[UploadStatus] = Field(None, description="Filter by processing status")
    user_id: Optional[int] = Field(None, description="Filter by user")
    limit: int = Field(10, description="Maximum number of results") 