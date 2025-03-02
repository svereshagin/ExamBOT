from typing import Any, List, Dict, Sequence, Union
from sqlalchemy import ScalarResult, Row
from sqlalchemy.ext.asyncio import AsyncSession
from bot.app.repositories.models import Student, Exam
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
    async def get_report(cls, session: AsyncSession) -> Sequence[Row[tuple[Student, Exam]]] | None:
        """
        Читаем таблицу Students и Exam при помощи join
        Example:
            (<bot.app.repositories.models.Student object at 0x10522af30>, <bot.app.repositories.models.Exam object at 0x10522af60>)
        """
        stmt = (
            select(Student, Exam)
            .join(Exam, Student.id == Exam.student_id)  # Соединяем таблицы по student_id
        )

        result = await session.execute(stmt)
        student_exam_pairs = result.all()
        print(type)# Получаем все пары (студент, экзамен)
        return student_exam_pairs

    @classmethod
    @connection
    async def create_students(cls, session: AsyncSession, students: List[str], form_exams: List[FormExam]) -> dict:
        print("create_students")
        try:
            for idx, student_name in enumerate(students):
                if idx >= len(form_exams):
                    break  # Если студентов больше, чем экзаменов

                new_student = Student(surname=student_name)
                session.add(new_student)
                await session.flush()  # Обновляем сессию, чтобы получить ID нового студента

                exam = Exam(
                    turn=form_exams[idx].turn,
                    examination_paper=form_exams[idx].examination_paper,
                    tasks="\n".join(form_exams[idx].tasks),
                    student_id=new_student.id,  # Теперь ID доступен
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
    async def get_all_students(cls, session: AsyncSession) -> Union[List[Student], dict]:
        """
        Возвращает список обьектов класса Student, либо возвращает словарь с ошибкой
        """
        try:
            stmt = select(Student)
            result = await session.execute(stmt)
            student_exam_pairs = result.scalars().all()  # Извлекаем только объекты Student
            list_of_students = []
            for student in student_exam_pairs:
                list_of_students.append(student)
            return student_exam_pairs
        except Exception as e:
            await session.rollback()
            return {"success": False, "error": str(e)}


# import asyncio
#
# students = ['adad', 'asda', 'asda12']
# form_questions.students = students
# form_exams = form_questions.form_groups()
# print(form_exams)
#
# s = StudentExam()
#
# async def call():
#     # res = await s.create_students(students=students, form_exams=form_exams)
#     # R = await s.get_report()
#     # from bot.app.services.report import make_resulted_report, make_telegram_report
#     # R = make_resulted_report(R)
#     # R = make_telegram_report(R)
#     # for i in R:
#     #     print(i)
#     r1 = await s.get_all_students()
#     print(r1)
#     for i in r1:
#         print(i.surname)
#
# # Запускаем асинхронную функцию
# async def main():
#     res1 = await call()
#     print(res1)
#
# # Запускаем основной асинхронный контекст
# if __name__ == "__main__":
#     asyncio.run(main())

student_exams = StudentExam()
