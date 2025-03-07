from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.app.logger.logger_file import logger
from bot.app.repositories.database import connection
from bot.app.repositories.models import Teacher, Student, Exam
from bot.app.services.Exam.form_questions import FormExam


@connection
async def add_students(
        cls, session: AsyncSession, telegram_id: int, students: List[str], form_exams: List[FormExam]
) -> dict:
    try:
        # Получаем учителя
        teacher = await session.scalar(
            select(Teacher).where(Teacher.telegram_id == telegram_id)
        )
        if not teacher:
            return {"error": "Teacher not found"}

        # Создаем всех студентов и экзамены
        students_and_exams = []
        for student_name, exam_data in zip(students, form_exams):
            student = Student(surname=student_name, teacher_id=teacher.id)
            exam = Exam(
                turn=exam_data.turn,
                examination_paper=exam_data.examination_paper,
                tasks="\n".join(exam_data.tasks),
                student=student  # Используем relationship вместо student_id
            )
            students_and_exams.extend([student, exam])

        session.add_all(students_and_exams)
        await session.commit()

        return {"success": True}
    except Exception as e:
        await session.rollback()
        logger.error(f"Error: {e}", exc_info=True)
        return {"error": str(e)}


