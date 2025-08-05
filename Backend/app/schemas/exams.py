from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum
from .materials import Subject

class ExamYear(str, Enum):
    YEAR_2014 = "2014"
    YEAR_2015 = "2015"
    YEAR_2016 = "2016"
    YEAR_2017 = "2017"
    YEAR_2018 = "2018"
    YEAR_2019 = "2019"
    YEAR_2020 = "2020"
    YEAR_2021 = "2021"
    YEAR_2022 = "2022"
    YEAR_2023 = "2023"
    YEAR_2024 = "2024"

class ExamType(str, Enum):
    EUEE = "euee"
    MOCK = "mock"
    PRACTICE = "practice"

class ExamBase(BaseModel):
    title: str = Field(..., description="Exam title")
    year: ExamYear = Field(..., description="Year of the exam")
    subject: Subject = Field(..., description="Subject of the exam")
    exam_type: ExamType = Field(..., description="Type of exam")
    file_path: str = Field(..., description="Path to the exam file")
    file_size: Optional[int] = Field(None, description="File size in bytes")
    duration_minutes: Optional[int] = Field(None, description="Exam duration in minutes")
    total_marks: Optional[int] = Field(None, description="Total marks for the exam")
    description: Optional[str] = Field(None, description="Description of the exam")
    is_solution_available: bool = Field(False, description="Whether solution is available")

class ExamCreate(ExamBase):
    pass

class Exam(ExamBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ExamSearch(BaseModel):
    query: Optional[str] = Field(None, description="Search query")
    year: Optional[ExamYear] = Field(None, description="Filter by year")
    subject: Optional[Subject] = Field(None, description="Filter by subject")
    exam_type: Optional[ExamType] = Field(None, description="Filter by exam type")
    limit: int = Field(10, description="Maximum number of results")

class ExamSolution(BaseModel):
    exam_id: int = Field(..., description="ID of the exam")
    file_path: str = Field(..., description="Path to the solution file")
    file_size: Optional[int] = Field(None, description="File size in bytes")
    description: Optional[str] = Field(None, description="Description of the solution")

class ExamSolutionCreate(ExamSolution):
    pass

class ExamSolutionResponse(ExamSolution):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True 