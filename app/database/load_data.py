from app.database.database import SessionLocal
from app.database.models import Student, FacultyMember, Course

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
    db.flush()  # Flush to get the IDs of faculty members for course assignment

    # Load Courses
    courses = [
        Course(title="Introduction to Programming", description="Learn the basics of programming.", credits=3, faculty_member_id=faculty_members[0].id),
        Course(title="Calculus I", description="An introduction to calculus.", credits=4, faculty_member_id=faculty_members[1].id),
        Course(title="Physics I", description="Fundamentals of physics.", credits=4, faculty_member_id=faculty_members[2].id),
    ]
    db.add_all(courses)

    db.commit()
    db.close()