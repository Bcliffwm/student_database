from typing import Optional, List
from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
        unique=True
    )

    name: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
        index=True
    )

    major: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )

    gpa: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True
    )

    enrollments: Mapped[List["Enrollment"]] = relationship(
        "Enrollment",
        back_populates="student"
    )


class FacultyMember(Base):
    __tablename__ = "faculty_members"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
        unique=True
    )

    name: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
        index=True
    )

    department: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )

    title: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )

    # One faculty member can teach multiple courses
    courses: Mapped[List["Course"]] = relationship(
        "Course",
        back_populates="faculty_member"
    )


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
        unique=True
    )

    title: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
        index=True
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )
    
    credits: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True
    )

    # Foreign key referencing FacultyMember
    faculty_member_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("faculty_members.id"),
        nullable=True
    )

    # Each course belongs to one faculty member
    faculty_member: Mapped[Optional["FacultyMember"]] = relationship(
        "FacultyMember",
        back_populates="courses"
    )

class Enrollment(Base):
    __tablename__ = "enrollments"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    student_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("students.id"),
        nullable=False
    )

    course_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("courses.id"),
        nullable=False
    )

    semester: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    grade: Mapped[Optional[str]] = mapped_column(
        String(2),
        nullable=True
    )
    enrollment_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    student: Mapped["Student"] = relationship("Student", back_popluates="enrollments")
    course: Mapped["Course"] = relationship("Course", back_popluates="enrollments")