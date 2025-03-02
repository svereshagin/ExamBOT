from typing import Sequence

from sqlalchemy import Row

from bot.app.repositories.models import Student, Exam


def make_resulted_report(student_exam_pairs: Sequence[Row[tuple[Student, Exam]]] | None):
    """
    Возвращает список словарей типа
    {'surname': 'Жуков', 'mark': 0, 'turn': 21, 'examination_paper': 2}
    получает последовательность из StudentExam().get_report()
    Example:
        R = await s.get_report()
        R = make_resulted_report(R)
        for i in R:
            print(i)
    """
    student_info = []

    for student, exam in student_exam_pairs:
        student_info.append({
            "surname": student.surname,
            "mark": exam.mark,
            "turn": exam.turn,
            "examination_paper": exam.examination_paper  # Номер экзаменационного билета
        })

    return student_info

def make_telegram_report(students: list[dict[str,int,int,int]]):
    """
    R = await s.get_report()
    R = make_resulted_report(R)
    R = make_telegram_report(R)

    result:
        surname: asda mark: 0
        turn: 0
        examination_paper: 1
    """
    list_of_str_students = []
    print(students)
    for elem in students:
        str_student = f'Фамилия: {elem["surname"]} \n Оценка: {elem["mark"]} \n Очередь: {elem["turn"]} \n Номер экз.билета: {elem["examination_paper"]}'
        list_of_str_students.append(str_student)
    print(list_of_str_students)
    return list_of_str_students
