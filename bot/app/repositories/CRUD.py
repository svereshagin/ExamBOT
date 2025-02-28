from typing import Any, List
from sqlalchemy import ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from bot.app.repositories.models import Student, Exam
from bot.app.repositories.database import connection

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
    async def get_all_students(cls, session: AsyncSession) -> ScalarResult[Any]:
        return await session.scalars(Student)

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
#     res = await s.create_students(students=students, form_exams=form_exams)
#     return res
#
# # Запускаем асинхронную функцию
# async def main():
#     res1 = await call()
#     print(res1)
#
# # Запускаем основной асинхронный контекст
# if __name__ == "__main__":
#     asyncio.run(main())
# Сохраняем все изменения в базе данных

    # Пример использования
    # Предположим, у нас есть сессия SQLAlchemy и студент

        #     async def register_user(cls, telegram_id: int, name: str, language: str, username: str, password: str,


#                             session: AsyncSession):
#         """Добавляет нового пользователя с профилем и учетными данными в базу данных."""
#
#         # Проверяем, есть ли уже такой пользователь
#         existing_user = await session.scalar(
#             select(Student).where(Student.telegram_id == telegram_id)
#         )
#         if existing_user:
#             return False  # Пользователь уже существует
#
#         # Если проверки пройдены, создаем пользователя
#         student = Student(telegram_id=telegram_id)
#         credential = Credential(username=username, password=password, student=student)
#         profile = Profile(name=name, language=language, student=student)
#
#         # Добавляем в сессию
#         session.add(student)
#         session.add(credential)
#         session.add(profile)
#
#         # Коммитим изменения
#         await session.commit()
#         return {"success": True}  # Успешно зарегистрирован
#
#     @staticmethod
#     @connection
#     async def get_telegram_user_by_id(telegram_id: int, session: AsyncSession):
#         try:
#             stmt = select(Student).where(Student.telegram_id == telegram_id)
#             request = await session.scalars(stmt)  # Используем await для выполнения запроса
#             return request.first()  # Возвращаем первый результат или None
#         except Exception as e:
#             print(e)
#             return None  # Возвращаем None в случае ошибки
#
#
# class UserProfile:
#     @classmethod
#     @connection
#     async def get_profile(cls, user_id: int, session: AsyncSession):
#         # Находим существующего пользователя
#         existing_user = await session.scalar(
#             select(Student).where(Student.telegram_id == user_id)
#         )
#
#         if not existing_user:
#             return None  # Пользователь не существует
#
#         # Выполняем запрос с явным указанием соединений
#         result = await session.execute(
#             select(Profile, Credential)
#             .select_from(Student)
#             .join(Profile, Profile.student_id == Student.id)
#             .join(Credential, Credential.student_id == Student.id)
#             .where(Student.id == existing_user.id)
#         )
#
#         profiles_with_credentials = result.all()  # Получаем все профили и учетные данные
#
#         if not profiles_with_credentials:
#             return None  # Если профили или учетные данные не найдены
#
#         # Формируем список с данными
#         profiles = []
#         for profile, credential in profiles_with_credentials:
#             profiles.append({
#                 'name': profile.name,
#                 'language': profile.language,
#                 'username': credential.username,
#                 'password': credential.password
#             })
#
#         return profiles  # Возвращаем список профилей с учетными данными

student_exams = StudentExam()
