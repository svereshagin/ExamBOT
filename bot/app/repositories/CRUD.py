from typing import Any, List, Dict, Sequence, Union
from sqlalchemy import ScalarResult, Row, delete
from sqlalchemy.ext.asyncio import AsyncSession
from bot.app.repositories.models import Student, Exam, Teacher
from bot.app.repositories.database import connection
from sqlalchemy import select
from bot.app.services.Exam.form_questions import FormExam, form_questions


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
        cls, session: AsyncSession
    ) -> Sequence[Row[tuple[Student, Exam]]] | None:
        """
        Читаем таблицу Students и Exam при помощи join
        Example:
            (<bot.app.repositories.models.Student object at 0x10522af30>, <bot.app.repositories.models.Exam object at 0x10522af60>)
        """
        stmt = select(Student, Exam).join(
            Exam, Student.id == Exam.student_id
        )  # Соединяем таблицы по student_id

        result = await session.execute(stmt)
        student_exam_pairs = result.all()
        print(type)  # Получаем все пары (студент, экзамен)
        return student_exam_pairs

    @classmethod
    @connection
    async def add_teacher(cls, session: AsyncSession, telegram_id: int) -> dict:
        """Добавляет учителя в базу данных по его Telegram ID."""
        try:
            # Проверяем, существует ли уже учитель с таким Telegram ID
            existing_teacher = await session.execute(
                Teacher.select().where(Teacher.telegram_id == telegram_id)
            )
            if existing_teacher.scalar_one_or_none():
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
    async def add_students(
            cls, session: AsyncSession, telegram_id: int, students: List[str], form_exams: List[FormExam]
    ) -> dict:
        """"Добавляет учеников в БД по teacher_id"""
        print("create_students")
        try:
            # Получаем учителя по telegram_id
            teacher = await session.execute(
                Teacher.select().where(Teacher.telegram_id == telegram_id)
            )
            teacher = teacher.scalar_one_or_none()
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
