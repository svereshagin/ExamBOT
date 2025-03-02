from bot.app.repositories.CRUD import student_exams
from typing import Optional, Tuple, List

class ExamTimerPreparations:
    def __init__(self, mode1: Optional[Tuple[int, int]] = None, mode2: Optional[Tuple[int, int]] = None):
        """
        Инициализирует параметры экзамена.

        :param mode1: Кортеж, содержащий время на подготовку и общее время экзамена.
        :param mode2: Кортеж, содержащий время на подготовку и время на одного студента.

        async def main():
            s = ExamTimerPreparations(mode1=(15, 120))
            result_text, result_data = await s.resulted_timer()  # Получаем текст и данные
            print(result_text)  # Выводим текст
            print(result_data)  # Выводим дополнительные данные
            # Запуск асинхронного кода
        asyncio.run(main())
        """
        self.preparation_time: Optional[int] = None
        self.exam_time: Optional[int] = None
        self.time_per_student: Optional[int] = None
        self.students: List[str] = []

        if mode1 and isinstance(mode1, tuple):
            self.preparation_time = mode1[0]
            self.exam_time = mode1[1]

        if mode2 and isinstance(mode2, tuple):
            self.preparation_time = mode2[0]
            self.time_per_student = mode2[1]

    async def initialize(self) -> None:
        """Асинхронный метод для инициализации студентов."""
        self.students = await self.get_students()

    async def get_students(self) -> List[str]:
        """Получает список студентов.

        :return: Список имен студентов.
        """
        return await student_exams.get_all_students()

    async def resulted_timer(self) -> Tuple[str, Tuple[Optional[int], Optional[int], Optional[int], int, List[str]]]:
        """Возвращает строку с результатами расчета времени на экзамен и дополнительные данные."""
        await self.initialize()

        if self.exam_time:  # Если выбран режим 1
            if len(self.students) > 0:  # Проверяем, есть ли студенты
                if self.exam_time > self.preparation_time:
                    self.time_per_student = (self.exam_time - self.preparation_time) / len(
                        self.students)  # Используем дробное деление

                    # Условие для минимального времени на студента
                    if self.time_per_student < 3:
                        self.time_per_student = 3  # Устанавливаем минимальное время на студента

                else:
                    self.time_per_student = 0  # Или установите другое значение по умолчанию

                result_text = (f"Время на одного студента: {self.time_per_student:.2f}, "
                               f"Общее время экзамена: {self.exam_time}, "
                               f"Время на подготовку: {self.preparation_time}, "
                               f"Количество студентов: {len(self.students)}")
                return result_text, (
                    self.exam_time, self.time_per_student, self.preparation_time, len(self.students), self.students)
            else:
                return "Нет студентов для расчета времени в режиме 1.", (
                    self.exam_time, self.time_per_student, self.preparation_time, 0, self.students)

        elif self.time_per_student:  # Если выбран режим 2
            if len(self.students) > 0:  # Проверяем, есть ли студенты
                self.exam_time = (self.time_per_student * len(self.students)) + self.preparation_time
                result_text = (f"Время на одного студента: {self.time_per_student}, "
                               f"Общее время экзамена: {self.exam_time}, "
                               f"Время на подготовку: {self.preparation_time}, "
                               f"Количество студентов: {len(self.students)}")
                return result_text, (
                    self.exam_time, self.time_per_student, self.preparation_time, len(self.students), self.students)
            else:
                return "Нет студентов для расчета времени в режиме 2.", (
                    self.exam_time, self.time_per_student, self.preparation_time, 0, self.students)

        return "Не указаны корректные параметры для расчета времени.", (None, None, None, 0, self.students)

