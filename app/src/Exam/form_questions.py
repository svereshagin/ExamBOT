import yaml
import pathlib
import random

class FormQuestions:
    __base_file = pathlib.Path(__file__).resolve().parents[2].joinpath('yml_files').joinpath('questions.yml')

    def __init__(self):
        self.data = self.get_content()
        self.number_of_exam_papers: int = len(self.data)
        self.already_used = []

    def get_content(self) -> list:
        """returns a list of questions out of yml_files/questions.yml"""
        try:
            with open(self.__base_file, 'r', encoding='UTF-8') as file:
                data = yaml.safe_load(file)
                return data or []  # Возвращаем пустой список, если файл пуст
        except FileNotFoundError:
            print(f"Error: The file {self.__base_file} was not found.")
            return []
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file: {e}")
            return []

    def randomize_exam_paper_per_student(self) -> int:
        """return a randomized_exam_paper_q, if already"""
        if len(self.already_used) >= self.number_of_exam_papers:
            return random.choice(self.already_used)

        while True:
            salt = random.randint(1, self.number_of_exam_papers)
            if salt not in self.already_used:
                self.already_used.append(salt)
                return salt

    def form_exam_questions(self) -> list:
        #лучше тогда по числам просто итерировать исправить после больницы
        return self.data[f'num{self.randomize_exam_paper_per_student()}']

s: FormQuestions = FormQuestions()
