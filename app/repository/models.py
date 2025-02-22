from sqlalchemy import VARCHAR, ForeignKey, INT, TEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.repository.database import Base
from typing_extensions import Annotated
from pydantic import BaseModel, StringConstraints, validator, ValidationError



class Student(Base):
    surname: Mapped[str] = mapped_column(VARCHAR)
    created_at = None
    updated_at = None
    credentials: Mapped['Exam'] = relationship(
        back_populates="student", uselist=False, cascade="all, delete-orphan"
    )



class Exam(Base):
    mark: Mapped[str] = mapped_column(INT)
    turn: Mapped[str] = mapped_column(INT)
    examination_paper: Mapped[int] = mapped_column(INT) #номер экзаменационного билета
    tasks: Mapped[str] = mapped_column(TEXT) #задания с этого билета
    student_id: Mapped[int] = mapped_column(
        INT, ForeignKey('students.id'), unique=True, nullable=False
    )





