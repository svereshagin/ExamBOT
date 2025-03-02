import pytest
from unittest.mock import patch, AsyncMock
from bot.app.services.Exam.timer import ExamTimerPreparations  # Замените на фактическое имя вашего модуля


@pytest.mark.asyncio
async def test_resulted_timer_mode1_with_students():
    # Мокаем метод получения студентов
    with patch('bot.app.repositories.CRUD.student_exams.get_all_students', new_callable=AsyncMock) as mock_get_students:
        mock_get_students.return_value = ['Student A', 'Student B', 'Student C']

        exam_timer = ExamTimerPreparations(mode1=(15, 120))
        result_text, result_data = await exam_timer.resulted_timer()

        assert result_text == "Время на одного студента: 35, Общее время экзамена: 120, Время на подготовку: 15, Количество студентов: 3"
        assert result_data == (120, 35, 15, 3, ['Student A', 'Student B', 'Student C'])


@pytest.mark.asyncio
async def test_resulted_timer_mode1_no_students():
    with patch('bot.app.repositories.CRUD.student_exams.get_all_students', new_callable=AsyncMock) as mock_get_students:
        mock_get_students.return_value = []

        exam_timer = ExamTimerPreparations(mode1=(15, 120))
        result_text, result_data = await exam_timer.resulted_timer()

        assert result_text == "Нет студентов для расчета времени в режиме 1."
        assert result_data == (120, None, 15, 0, [])


@pytest.mark.asyncio
async def test_resulted_timer_mode2_with_students():
    with patch('bot.app.repositories.CRUD.student_exams.get_all_students', new_callable=AsyncMock) as mock_get_students:
        mock_get_students.return_value = ['Student A', 'Student B']

        exam_timer = ExamTimerPreparations(mode2=(15, 30))
        result_text, result_data = await exam_timer.resulted_timer()

        assert result_text == "Время на одного студента: 30, Общее время экзамена: 75, Время на подготовку: 15, Количество студентов: 2"
        assert result_data == (75, 30, 15, 2, ['Student A', 'Student B'])


@pytest.mark.asyncio
async def test_resulted_timer_mode2_no_students():
    with patch('bot.app.repositories.CRUD.student_exams.get_all_students', new_callable=AsyncMock) as mock_get_students:
        mock_get_students.return_value = []

        exam_timer = ExamTimerPreparations(mode2=(15, 30))
        result_text, result_data = await exam_timer.resulted_timer()

        assert result_text == "Нет студентов для расчета времени в режиме 2."
        assert result_data == (None, 30, 15, 0, [])

# @pytest.mark.asyncio
# async def test_resulted_timer_no_mode():
#     exam_timer = ExamTimerPreparations()
#     result_text, result_data = await exam_timer.resulted_timer()
#
#     assert result_text == "Не указаны корректные параметры для расчета времени."
#     assert result_data == (None, None, None, 0, [])
