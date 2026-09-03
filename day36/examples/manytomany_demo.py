# Day 36 多对多关系示例
from sqlalchemy import create_engine, Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

engine = create_engine('sqlite:///:memory:')
Session = sessionmaker(bind=engine)
Base = declarative_base()

# 多对多关联表
student_course = Table(
    'student_course', Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id')),
    Column('course_id', Integer, ForeignKey('courses.id')),
)

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    courses = relationship('Course', secondary=student_course, back_populates='students')

class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    students = relationship('Student', secondary=student_course, back_populates='courses')

Base.metadata.create_all(engine)

session = Session()
alice = Student(name='Alice')
math = Course(title='Math')
python = Course(title='Python')
alice.courses.extend([math, python])
session.add(alice)
session.commit()

# 查询 Alice 的所有课程
student = session.query(Student).filter_by(name='Alice').first()
print(f"{student.name} courses: {[c.title for c in student.courses]}")

# 查询 Math 课程的所有学生
course = session.query(Course).filter_by(title='Math').first()
print(f"{course.title} students: {[s.name for s in course.students]}")
session.close()
