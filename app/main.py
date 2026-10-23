from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Query, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models
from app.database import Base, engine, get_db
from app.schemas import StudentCreate, StudentRead, StudentUpdate
from app.schemas import FacultyMemberCreate, FacultyMemberRead, FacultyMemberUpdate
from app.schemas import CourseCreate, CourseRead, CourseUpdate


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

# Setting up FastAPI application with title and lifespan context manager
app = FastAPI(title="Docker Database API", lifespan=lifespan)


# Checking app health status
@app.get("/health")
def health_check():
    return {"status": "ok"}

# CRUD operations for Database Entities: Students, Faculty Members, and Courses

# Create operations for Database Entities: Students, Faculty Members, and Courses
@app.post("/students", response_model=StudentRead, status_code=status.HTTP_201_CREATED)
def create_student(payload: StudentCreate, db: Session = Depends(get_db)):
    student = models.Student(**payload.model_dump())
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

@app.post("/faculty_members", response_model=FacultyMemberRead, status_code=status.HTTP_201_CREATED)
def create_faculty_member(payload: FacultyMemberCreate, db: Session = Depends(get_db)):
    faculty_member = models.FacultyMember(**payload.model_dump())
    db.add(faculty_member)
    db.commit()
    db.refresh(faculty_member)
    return faculty_member

@app.post("/courses", response_model=CourseRead, status_code=status.HTTP_201_CREATED)
def create_course(payload: CourseCreate, db: Session = Depends(get_db)):
    course = models.Course(**payload.model_dump())
    db.add(course)
    db.commit()
    db.refresh(course)
    return course

# Listing Entities: Students, Faculty Members, and Courses
@app.get("/students", response_model=list[StudentRead])
def list_students(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    db: Session = Depends(get_db),
):
    statement = select(models.Student).order_by(models.Student.id).offset(offset).limit(limit)
    return db.scalars(statement).all()

@app.get("/faculty_members", response_model=list[FacultyMemberRead])
def list_faculty_members(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    db: Session = Depends(get_db),
):
    statement = select(models.FacultyMember).order_by(models.FacultyMember.id).offset(offset).limit(limit)
    return db.scalars(statement).all()

@app.get("/courses", response_model=list[CourseRead])
def list_courses(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    db: Session = Depends(get_db),
):
    statement = select(models.Course).order_by(models.Course.id).offset(offset).limit(limit)
    return db.scalars(statement).all()

# Retreive Operations for Database Entities: Students, Faculty Members, and Courses
@app.get("/students/{student_id}", response_model=StudentRead)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.get(models.Student, student_id)
    if student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return student

@app.get("/faculty_members/{faculty_member_id}", response_model=FacultyMemberRead)
def get_faculty_member(faculty_member_id: int, db: Session = Depends(get_db)):
    faculty_member = db.get(models.FacultyMember, faculty_member_id)
    if faculty_member is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Faculty member not found")
    return faculty_member

@app.get("/courses/{course_id}", response_model=CourseRead)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.get(models.Course, course_id)
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return course

# Update Operations for Database Entities: Students, Faculty Members, and Courses
@app.patch("/students/{student_id}", response_model=StudentRead)
def update_student(student_id: int, payload: StudentUpdate, db: Session = Depends(get_db)):
    student = db.get(models.Student, student_id)
    if student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    for field, value in payload.model_dump(exclude_unset=True).students():
        setattr(student, field, value)
    db.commit()
    db.refresh(student)
    return student

@app.patch("/faculty_members/{faculty_member_id}", response_model=FacultyMemberRead)
def update_faculty_member(faculty_member_id: int, payload: FacultyMemberUpdate, db: Session = Depends(get_db)):
    faculty_member = db.get(models.FacultyMember, faculty_member_id)
    if faculty_member is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Faculty member not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(faculty_member, field, value)
    db.commit()
    db.refresh(faculty_member)
    return faculty_member

@app.patch("/courses/{course_id}", response_model=CourseRead)
def update_course(course_id: int, payload: CourseUpdate, db: Session = Depends(get_db)):
    course = db.get(models.Course, course_id)
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(course, field, value)
    db.commit()
    db.refresh(course)
    return course

# Delete Operations for Database Entities: Students, Faculty Members, and Courses
@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.get(models.Student, student_id)
    if student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    db.delete(student)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.delete("/faculty_members/{faculty_member_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_faculty_member(faculty_member_id: int, db: Session = Depends(get_db)):
    faculty_member = db.get(models.FacultyMember, faculty_member_id)
    if faculty_member is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Faculty member not found")
    db.delete(faculty_member)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.delete("/courses/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.get(models.Course, course_id)
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    db.delete(course)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)