from typing import List, Sequence, Union
from sqlalchemy import  Row
from bot.app.logger.logger_file import logger
from bot.app.repositories.models import Student, Exam, Teacher
from bot.app.repositories.database import connection
from bot.app.services.Exam.form_questions import FormExam
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class StudentExam:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = True
            return object.__new__(cls)
        else:
            raise Exception("This class is a singleton!")

    @classmethod
    @connection
    async def add_teacher(cls, session: AsyncSession, telegram_id) -> dict:
        """
        Add a teacher to the database.
        Args:
            session:
            telegram_id:

        Returns:
            dict {"success": True} if OK
            dict {"success": False, "error": "Teacher with {teacher.telegram_id} already exists"}}
        """
        try:
            logger.info(f"Adding teacher {telegram_id}")

            # Проверка существующего учителя
            stmt = select(Teacher).where(Teacher.telegram_id == telegram_id)
            result = await session.execute(stmt)
            teacher = result.scalar_one_or_none()

            # Если учитель не найден
            if not teacher:
                new_teacher = Teacher(telegram_id=telegram_id)
                session.add(new_teacher)
                await session.commit()  # Фиксируем изменения
                await session.refresh(new_teacher)  # Обновляем атрибуты (если нужно ID)
                logger.debug(f"Created new teacher: {new_teacher.telegram_id}")
                result = {"success": True}
            else:
                result = {"success": False, "error": f"Teacher with {teacher.telegram_id} already exists"}
            logger.debug(f"Teacher already exists: {telegram_id}")
            return result



        except Exception as e:
            logger.error(f"Error adding teacher: {e}")
            await session.rollback()  # Откатываем транзакцию при ошибке
            raise  # Пробрасываем исключение дальше

    @classmethod
    @connection
    async def get_report(
            cls, session: AsyncSession, telegram_id: int
    ) -> Sequence[Row[tuple[Student, Exam]]] | None:
        """
        Получает отчёт по ученикам и их экзаменам для выбранного учителя по telegram_id.
        """
        try:
            # Получаем всех студентов для учителя с указанным telegram_id
            stmt = (
                select(Student, Exam)
                .join(Teacher, Teacher.id == Student.teacher_id)
                .join(Exam, Student.id == Exam.student_id)
                .where(Teacher.telegram_id == telegram_id)
            )  # Соединяем таблицы по student_id и фильтруем по telegram_id

            result = await session.execute(stmt)
            student_exam_pairs = result.all()  # Получаем все пары (студент, экзамен)

            if student_exam_pairs:
                return student_exam_pairs
            else:
                return None  # Если нет студентов, возвращаем None

        except Exception as e:
            return {"success": False, "error": str(e)}



    @classmethod
    @connection
    async def delete_all_students_for_teacher_by_telegram_id(cls, session: AsyncSession, telegram_id: int) -> dict:
        """Удаляет всех учеников у выбранного учителя по telegram_id"""
        try:
            # Получаем всех студентов для учителя с указанным telegram_id
            stmt = (
                select(Student)
                .join(Teacher)
                .where(Teacher.telegram_id == telegram_id)
            )
            result = await session.execute(stmt)
            students = result.scalars().all()

            # Удаляем студентов
            if students:
                for student in students:
                    await session.delete(student)
                await session.commit()  # Совершаем все изменения за один раз
                return {"success": True, "message": "Students deleted successfully."}
            else:
                return {"success": False, "message": "No students found for this teacher."}

        except Exception as e:
            await session.rollback()  # Откатить изменения в случае ошибки
            return {"success": False, "error": str(e)}


    #TODO добавить в ведомости
    @classmethod
    @connection
    async def get_students_by_teacher_telegram_id(cls, session: AsyncSession, telegram_id: int) -> dict:
        """Получает всех учеников для выбранного учителя по telegram_id"""
        try:
            # Проверяем наличие учителя с таким telegram_id
            teacher_check_stmt = select(Teacher).where(Teacher.telegram_id == telegram_id)
            teacher_result = await session.execute(teacher_check_stmt)
            teacher = teacher_result.scalars().first()

            if not teacher:
                return {"success": False, "message": "Teacher not found with the given telegram_id."}

            # Получаем всех студентов для учителя с указанным telegram_id
            stmt = (
                select(Student)
                .where(Student.teacher_id == teacher.id)
            )
            result = await session.execute(stmt)
            students = result.scalars().all()

            if students:
                return {"success": True, "students": students}
            else:
                return {"success": False, "message": "No students found for this teacher."}

        except Exception as e:
            return {"success": False, "error": str(e)}

    @classmethod
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

    @classmethod
    @connection
    async def get_all_students(
        cls, session: AsyncSession
    ) -> Union[List[Student], dict]:
        """
        Возвращает список обьектов класса Student, либо возвращает словарь с ошибкой
        """
        try:
            stmt = select(Student)
            result = await session.execute(stmt)
            student_exam_pairs = (
                result.scalars().all()
            )  # Извлекаем только объекты Student
            list_of_students = []
            for student in student_exam_pairs:
                list_of_students.append(student)
            return student_exam_pairs
        except Exception as e:
            await session.rollback()
            return {"success": False, "error": str(e)}

    @classmethod
    @connection
    async def delete_all_students(cls, session: AsyncSession) -> Union[None, dict]:
        # try:
        #     stmt = delete(Student).whe
        pass


student_exams = StudentExam()


# async def main():
#     # await get_teacher(tg_id=7084142136)
#     res = await student_exams.get_report(telegram_id=7084142136)
#     print(res)
#
#
#
#
# if __name__ == '__main__':
#     asyncio.run(main())
