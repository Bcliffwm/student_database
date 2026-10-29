from contextlib import asynccontextmanager
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Query, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import models
from app.database.database import Base, engine, get_db
from app.database.schemas import StudentCreate, StudentRead, StudentUpdate
from app.database.schemas import FacultyMemberCreate, FacultyMemberRead, FacultyMemberUpdate
from app.database.schemas import CourseCreate, CourseRead, CourseUpdate
from app.database.schemas import EnrollmentCreate, EnrollmentRead, EnrollmentUpdate
from app.database.load_data import load_data, check_database


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")

    # Check to see if database file already has data
    if not check_database():    
        print("Loading initial data into the database...")
        load_data()  # Load initial data into the database
    yield

# Initialize FastAPI
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

@app.post("/enrollments", response_model=EnrollmentRead, status_code=status.HTTP_201_CREATED)
def create_enrollment(payload: EnrollmentCreate, db: Session = Depends(get_db)):
    if db.get(models.Student, payload.student_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    if db.get(models.Course, payload.course_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    enrollment = models.Enrollment(**payload.model_dump())
    db.commit()
    db.refresh(enrollment)
    return enrollment

# Listing Entities: Students, Faculty Members, and Courses
@app.get("/students", response_model=List[StudentRead])
def list_students(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    db: Session = Depends(get_db),
):
    statement = select(models.Student).order_by(models.Student.id).offset(offset).limit(limit)
    return db.scalars(statement).all()

@app.get("/faculty_members", response_model=List[FacultyMemberRead])
def list_faculty_members(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    db: Session = Depends(get_db),
):
    statement = select(models.FacultyMember).order_by(models.FacultyMember.id).offset(offset).limit(limit)
    return db.scalars(statement).all()

@app.get("/courses", response_model=List[CourseRead])
def list_courses(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    db: Session = Depends(get_db),
):
    statement = select(models.Course).order_by(models.Course.id).offset(offset).limit(limit)
    return db.scalars(statement).all()

@app.get("/enrollments", response_model=List[EnrollmentRead])
def list_enrollments(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    db: Session = Depends(get_db),
):
    statement = select(models.Enrollment).order_by(models.Enrollment.id).offset(offset).limit(limit)
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

@app.get("/enrollments/{enrollment_id}", response_model=EnrollmentRead)
def get_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    enrollment = db.get(models.Enrollment, enrollment_id)
    if enrollment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enrollment not found")
    return enrollment

# Update Operations for Database Entities: Students, Faculty Members, and Courses
@app.patch("/students/{student_id}", response_model=StudentRead)
def update_student(student_id: int, payload: StudentUpdate, db: Session = Depends(get_db)):
    student = db.get(models.Student, student_id)
    if student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
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

@app.patch("/enrollments/{enrollment_id}", response_model=EnrollmentRead)
def update_enrollment(enrollment_id: int, payload: EnrollmentUpdate, db: Session = Depends(get_db)):
    enrollment = db.get(models.Enrollment, enrollment_id)
    if enrollment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enrollment not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(enrollment, field, value)
    db.commit()
    db.refresh(enrollment)
    return enrollment

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

@app.delete("/enrollments/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    enrollment = db.get(models.Enrollment, enrollment_id)
    if enrollment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enrollment not found")
    db.delete(enrollment)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)