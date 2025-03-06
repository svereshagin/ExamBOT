from sqlalchemy import VARCHAR, ForeignKey, INT, TEXT, BIGINT
from sqlalchemy.orm import Mapped, mapped_column, relationship
from bot.app.repositories.database import Base


class Teacher(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(INT, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BIGINT, unique=True)

    students: Mapped[list["Student"]] = relationship(
        back_populates="teacher", cascade="all, delete-orphan"
    )


class Student(Base):
    """принимает surname и teacher.id"""
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(INT, primary_key=True)
    surname: Mapped[str] = mapped_column(VARCHAR)
    created_at: Mapped[str] = mapped_column(VARCHAR, default="CURRENT_TIMESTAMP")
    updated_at: Mapped[str] = mapped_column(VARCHAR, default="CURRENT_TIMESTAMP")

    teacher_id: Mapped[int] = mapped_column(
        INT, ForeignKey("teachers.id"), nullable=False
    )
    teacher: Mapped["Teacher"] = relationship("Teacher", back_populates="students")

    exams: Mapped[list["Exam"]] = relationship(
        back_populates="student", cascade="all, delete-orphan"
    )


class Exam(Base):
    __tablename__ = "exams"

    id: Mapped[int] = mapped_column(INT, primary_key=True)
    mark: Mapped[int] = mapped_column(INT, default=0)
    turn: Mapped[int] = mapped_column(INT)
    examination_paper: Mapped[int] = mapped_column(INT)
    tasks: Mapped[str] = mapped_column(TEXT)

    student_id: Mapped[int] = mapped_column(
        INT, ForeignKey("students.id"), unique=True, nullable=False
    )
    student: Mapped["Student"] = relationship("Student", back_populates="exams")
