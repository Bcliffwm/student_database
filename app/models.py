from typing import Optional, List

from sqlalchemy import Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
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


class FacultyMember(Base):
    __tablename__ = "faculty_members"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
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
        autoincrement=True
    )

    name: Mapped[str] = mapped_column(
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