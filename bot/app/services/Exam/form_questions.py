import yaml
import pathlib
import random


class FormQuestions:
    __base_file = (
        pathlib.Path(__file__)
        .resolve()
        .parents[2]
        .joinpath("yml_files")
        .joinpath("questions.yml")
    )

    def __init__(self, number_of_students: int):
        self.data = self.get_content()
        self.number_of_exam_papers: int = len(self.data)
        self.already_used = []
        self.number_of_students = number_of_students
        self.exam_papers = self.generate_exam_papers()

    def get_content(self) -> list:
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

    def __randomize_exam_paper_per_student(self) -> int:
        """Return a randomized exam paper number, if already used"""
        if len(self.already_used) >= self.number_of_exam_papers:
            return random.choice(self.already_used)

        while True:
            salt = random.randint(1, self.number_of_exam_papers)
            if salt not in self.already_used:
                self.already_used.append(salt)
                return salt

    def __form_exam_questions(self) -> list:
        """Form exam questions based on a randomized number"""
        return self.data[f"num{self.__randomize_exam_paper_per_student()}"]

    def generate_exam_papers(self) -> dict:
        """Generate exam papers for each student"""
        return {f"student_{i + 1}": self.__form_exam_questions() for i in range(self.number_of_students)}

    def get_exam_papers(self) -> dict[str, list]:
        """Return the generated exam papers """
        return self.exam_papers


# Example usage
number_of_students = 5  # Specify the number of students
s = FormQuestions(number_of_students)
#print(s.get_exam_papers())
