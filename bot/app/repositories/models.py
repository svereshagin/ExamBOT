from sqlalchemy import VARCHAR, ForeignKey, INT, TEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship
from bot.app.repositories.database import Base

class Student(Base):
    __tablename__ = 'students'  # Не забудьте указать имя таблицы

    id: Mapped[int] = mapped_column(INT, primary_key=True)  # Добавляем первичный ключ
    surname: Mapped[str] = mapped_column(VARCHAR)
    created_at: Mapped[str] = mapped_column(VARCHAR, default='CURRENT_TIMESTAMP')  # Пример, как можно добавить временные метки
    updated_at: Mapped[str] = mapped_column(VARCHAR, default='CURRENT_TIMESTAMP')

    exams: Mapped["Exam"] = relationship(
        back_populates="student", cascade="all, delete-orphan"
    )

class Exam(Base):
    __tablename__ = 'exams'  # Не забудьте указать имя таблицы

    id: Mapped[int] = mapped_column(INT, primary_key=True)  # Добавляем первичный ключ
    mark: Mapped[int] = mapped_column(INT, default=0)
    turn: Mapped[int] = mapped_column(INT)
    examination_paper: Mapped[int] = mapped_column(INT)  # номер экзаменационного билета
    tasks: Mapped[str] = mapped_column(TEXT)  # задания с этого билета
    student_id: Mapped[int] = mapped_column(
        INT, ForeignKey("students.id"), unique=True, nullable=False
    )
    student = relationship("Student", back_populates="exams")
