from typing import Counter, List

import yaml
import pathlib
import random
from pydantic import BaseModel
from random import shuffle

class FormExam(BaseModel):
    mark: int = 0
    turn: int = 0
    examination_paper: int = 0
    tasks: list = []

class FormQuestions:
    """
         Инициализирует экземпляр класса FormQuestions.

        Usage:
            form_questions(students) - сеттер для получения списка студентов
            exam = form_questions.form_groups() - формирование обьектов состоящих из данных о студентах
        Args:
             number_of_students (int): Количество студентов, для которых будут созданы экзаменационные листы.
                 Например:
                    >>> form_questions(students)
                    >>> exam = form_questions.form_groups()


         Raises:
             ValueError: Если number_of_students меньше 1.
         """
    __base_file = (
        pathlib.Path(__file__)
        .resolve()
        .parents[2]
        .joinpath("yml_files")
        .joinpath("questions.yml")
    )
    def __init__(self):
        self.__data = self.__get_content()
        self.__students: list = []
        print(self.__data)

    def __get_content(self) -> list:
        """Returns a list of questions out of yml_files/questions.yml"""
        try:
            with open(self.__base_file, "r", encoding="UTF-8") as file:
                data = yaml.safe_load(file)
                return data or []  # Return an empty list if the file is empty
        except FileNotFoundError:
            print(f"Error: The file {self.__base_file} was not found.")
            return []
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file: {e}")
            return []

    @property
    def students(self):
        return self.__students

    @students.setter
    def students(self, students):
        if students and isinstance(students, list):
            shuffle(students)
            self.__students = students
        else:
            raise TypeError("students must be a list and must not be empty")

    def form_groups(self) -> List[FormExam]:
        """Формирует группы студентов и создает экземпляры FormExam"""
        exams = []
        used_questions = set()  # Хранит использованные вопросы

        for counter, student in enumerate(self.__students):
            # Получаем все доступные вопросы, исключая уже использованные
            available_questions = [q for q in self.__data.keys() if q not in used_questions]

            if not available_questions:
                #print("Недостаточно вопросов для всех студентов. Повторное использование вопросов.")
                available_questions = list(self.__data.keys())  # Если вопросов недостаточно, берем все

            # Рандомим вопросы для студента
            selected_question = random.choice(available_questions)
            used_questions.add(selected_question)  # Добавляем вопрос в использованные

            # Создаем экземпляр FormExam для студента
            exam = FormExam(turn=counter, examination_paper=selected_question, tasks=self.__data[selected_question])
            exams.append(exam)

        return exams





form_questions = FormQuestions()
