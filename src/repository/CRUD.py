from typing import Any
from sqlalchemy import ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.models import Student, Exam
from src.repository.database import connection


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

    @classmethod
    @connection
    async def insert_students(cls, users: list, turn: int, examination_paper: int, tasks: list, session: AsyncSession):
        for user in users:
            new_user: Student = Student(surname=user)
            exam: Exam = Exam(turn=turn,examination_paper=examination_paper,tasks='\n'.join(tasks), student_id=new_user.id)
            session.add(new_user)
            session.add(exam)
            await session.commit()
            return {"success": True}


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

registration = StudentExam()

