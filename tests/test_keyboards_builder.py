import pytest
from bot.app.keyboards.keyboards_builder import (
    KeyboardBuilder,
)  # Импортируйте сам класс


@pytest.fixture
def keyboard_builder_instance():
    # Создаем экземпляр KeyboardBuilder
    return KeyboardBuilder()


def test_startup_buttons(keyboard_builder_instance):
    # Проверяем, что метод возвращает список
    assert isinstance(keyboard_builder_instance.startup_buttons, list)
