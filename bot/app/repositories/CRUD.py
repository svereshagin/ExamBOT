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
    async def add_teacher(cls, session: AsyncSession, telegram_id: int) -> dict:
        """Добавляет учителя в базу данных по его Telegram ID."""
        try:
            # Проверяем, существует ли уже учитель с таким Telegram ID
            stmt = select(Teacher).where(Teacher.telegram_id == telegram_id)
            result = await session.execute(stmt)
            teacher = result.scalar_one_or_none()
            if teacher:
                return {"success": False, "error": "Teacher already exists"}

            # Создаем нового учителя
            new_teacher = Teacher(telegram_id=telegram_id)
            session.add(new_teacher)

            await session.commit()  # Фиксируем изменения
            return {"success": True, "teacher_id": new_teacher.id}
        except Exception as e:
            await session.rollback()  # Откатываем транзакцию в случае ошибки
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
        print("create_students")
        try:
            # Получаем учителя по telegram_id
            stmt = select(Teacher).where(Teacher.telegram_id == telegram_id)
            result = await session.execute(stmt)
            teacher = result.scalar_one_or_none()

            if not teacher:
                return {"success": False, "error": "Teacher not found"}

            for idx, student_name in enumerate(students):
                if idx >= len(form_exams):
                    break  # Если студентов больше, чем экзаменов, прекращаем цикл

                # Создаем ученика, привязывая его к учителю
                new_student = Student(
                    surname=student_name,
                    teacher_id=teacher.id  # Добавляем связь с учителем
                )
                session.add(new_student)
                await session.flush()  # Обновляем сессию, чтобы получить ID нового студента

                # Создаем экзамен для этого студента
                exam = Exam(
                    turn=form_exams[idx].turn,
                    examination_paper=form_exams[idx].examination_paper,
                    tasks="\n".join(form_exams[idx].tasks),
                    student_id=new_student.id,  # Привязываем к созданному студенту
                )
                session.add(exam)

            print("create_students2")
            await session.commit()  # Коммитим все изменения сразу

            # Проверка, добавились ли студенты
            added_students = await session.execute(select(Student).where(Student.teacher_id == teacher.id))
            logger.info(f"Добавлено студентов в БД: {len(added_students.scalars().all())}")

            return {"success": True}
        except Exception as e:
            await session.rollback()  # Откатить изменения в случае ошибки
            return {"success": False, "error": str(e)}

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
