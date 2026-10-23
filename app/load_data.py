from app.database import SessionLocal
from app.models import Student, FacultyMember, Course

def load_data():
    db = SessionLocal()

    # Load Students
    students = [
        Student(name="Alice", major="Computer Science", gpa=3.8),
        Student(name="Bob", major="Mathematics", gpa=3.5),
        Student(name="Charlie", major="Physics", gpa=3.9),
    ]
    db.add_all(students)

    # Load Faculty Members
    faculty_members = [
        FacultyMember(name="Dr. Smith", department="Computer Science", title="Professor"),
        FacultyMember(name="Dr. Johnson", department="Mathematics", title="Associate Professor"),
        FacultyMember(name="Dr. Lee", department="Physics", title="Assistant Professor"),
    ]
    db.add_all(faculty_members)

    # Load Courses
    courses = [
        Course(title="Introduction to Programming", description="Learn the basics of programming.", credits=3, faculty_member_id=1),
        Course(title="Calculus I", description="An introduction to calculus.", credits=4, faculty_member_id=2),
        Course(title="Physics I", description="Fundamentals of physics.", credits=4, faculty_member_id=3),
    ]
    db.add_all(courses)

    db.commit()
    db.close()