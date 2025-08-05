from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class GradeLevel(str, Enum):
    GRADE_9 = "9"
    GRADE_10 = "10"
    GRADE_11 = "11"
    GRADE_12 = "12"

class Subject(str, Enum):
    MATHEMATICS = "mathematics"
    PHYSICS = "physics"
    CHEMISTRY = "chemistry"
    BIOLOGY = "biology"
    ENGLISH = "english"
    HISTORY = "history"
    GEOGRAPHY = "geography"
    SAT = "SAT"
class MaterialBase(BaseModel):
    title: str = Field(..., description="Title of the study material")
    subject: Subject = Field(..., description="Subject of the material")
    grade_level: GradeLevel = Field(..., description="Grade level (9-12)")
    description: Optional[str] = Field(None, description="Description of the material")
    file_path: str = Field(..., description="Path to the material file")
    file_size: Optional[int] = Field(None, description="File size in bytes")
    file_type: str = Field(..., description="File type (pdf, docx, etc.)")

class MaterialCreate(MaterialBase):
    pass

class Material(MaterialBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ChapterBase(BaseModel):
    title: str = Field(..., description="Chapter title")
    material_id: int = Field(..., description="ID of the parent material")
    page_start: Optional[int] = Field(None, description="Starting page number")
    page_end: Optional[int] = Field(None, description="Ending page number")
    content_summary: Optional[str] = Field(None, description="Summary of chapter content")

class ChapterCreate(ChapterBase):
    pass

class Chapter(ChapterBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class MaterialSearch(BaseModel):
    query: str = Field(..., description="Search query")
    subject: Optional[Subject] = Field(None, description="Filter by subject")
    grade_level: Optional[GradeLevel] = Field(None, description="Filter by grade level")
    limit: int = Field(10, description="Maximum number of results") 