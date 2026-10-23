from datetime import datetime
# Using pydantic for data validation and serialization - explicitly defines what attributes and fields belong to each entity
from pydantic import BaseModel, ConfigDict, Field

# Defining Pydantic models to emmulate the database operations for each entity
class StudentCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    description: str | None = None


class StudentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    description: str | None = None


class StudentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    created_at: datetime

class FacultyMemberCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    department: str | None = None
    title: str | None = None
    courses: list[int] | None = None

class FacultyMemberUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    department: str | None = None
    title: str | None = None
    courses: list[int] | None = None

class FacultyMemberRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    department: str | None
    title: str | None
    courses: list[int] | None

class CourseCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    description: str | None = None
    faculty_member_id: int | None = None
    faculty_member: "FacultyMemberRead" | None = None

class CourseUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    description: str | None = None
    faculty_member_id: int | None = None
    faculty_member: "FacultyMemberRead" | None = None

class CourseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    faculty_member_id: int | None
    faculty_member: "FacultyMemberRead" | None