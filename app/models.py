from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    major: Mapped[str | None] = mapped_column(Text, nullable=True)
    gpa: Mapped[float | None] = mapped_column(nullable=True)

class FacultyMember(Base):
    __tablename__ = "faculty_members"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    department: Mapped[str | None] = mapped_column(Text, nullable=True)
    title: Mapped[str | None] = mapped_column(Text, nullable=True)
    courses: Mapped[list["Course"]] = mapped_column(relationship("Course", back_populates="faculty_member"))

class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    faculty_member_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("faculty_members.id"), nullable=True)
    faculty_member: Mapped["FacultyMember"] = mapped_column(relationship("FacultyMember", back_populates="courses"))