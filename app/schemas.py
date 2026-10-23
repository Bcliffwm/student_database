from typing import Optional, List

from pydantic import BaseModel, ConfigDict, Field


# ==========================================
# Student Schemas
# ==========================================

class StudentCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    major: Optional[str] = None
    gpa: Optional[float] = Field(default=None, ge=0.0, le=4.0)


class StudentUpdate(BaseModel):
    name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=120
    )
    major: Optional[str] = None
    gpa: Optional[float] = Field(default=None, ge=0.0, le=4.0)


class StudentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    major: Optional[str] = None
    gpa: Optional[float] = None


# ==========================================
# Faculty Member Schemas
# ==========================================

class FacultyMemberCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    department: Optional[str] = None
    title: Optional[str] = None


class FacultyMemberUpdate(BaseModel):
    name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=120
    )
    department: Optional[str] = None
    title: Optional[str] = None


class FacultyMemberRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    department: Optional[str] = None
    title: Optional[str] = None


# ==========================================
# Course Schemas
# ==========================================

class CourseCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    description: Optional[str] = None
    faculty_member_id: Optional[int] = None


class CourseUpdate(BaseModel):
    name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=120
    )
    description: Optional[str] = None
    faculty_member_id: Optional[int] = None


class CourseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str] = None
    faculty_member_id: Optional[int] = None


# ==========================================
# Nested Relationship Schemas
# ==========================================

class FacultyMemberWithCourses(FacultyMemberRead):
    courses: List[CourseRead] = Field(default_factory=list)


class CourseWithFaculty(CourseRead):
    faculty_member: Optional[FacultyMemberRead] = None