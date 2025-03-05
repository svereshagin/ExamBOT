from pathlib import Path
import yaml
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

path = Path(__file__).parent.joinpath("main_menu.yml")


class MainKeyboardManager:
    def __init__(self):
        """
        При инициализации заполняет из файла main_menu.yml
        Ожидается, что файл main_menu.yml будет в той же директории (если не будет
        изменён path, что и файл KeyboardManager

        Возвращает клавиатуры как атрибуты класса через property
        """
        self.__data_low_kb: list = self.__read_yml_main_menu("low")
        self.__data_high_kb: dict[list] = self.__read_yml_main_menu("high")
        self.__button_stop: dict[list] = self.__read_yml_main_menu("stop")

    def __read_yml_main_menu(self, mode):
        """Читает YAML и загружает данные."""
        with open(path, encoding="utf-8", mode="r") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            return data[mode]

    def __make_reply_keyboard(self) -> ReplyKeyboardMarkup:
        """Создаёт обычную (нижнюю) клавиатуру."""
        keyboard = [[KeyboardButton(text=item)] for item in self.__data_low_kb]
        return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

    def __make_inline_keyboard(self) -> InlineKeyboardMarkup:
        """Создаёт инлайн-клавиатуру."""
        keyboard_data = dict(
            zip(self.__data_high_kb["text"], self.__data_high_kb["callback_queries"])
        )
        keyboard = [
            [InlineKeyboardButton(text=text, callback_data=callback)]
            for text, callback in keyboard_data.items()
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    def __make_inline_stop_keyboard(self) -> InlineKeyboardMarkup:
        """Создаёт инлайн-клавиатуру для остановки ввода."""
        keyboard = [
            [InlineKeyboardButton(text=text, callback_data=callback)]
            for text, callback in zip(
                self.__button_stop["text"], self.__button_stop["callback_queries"]
            )
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @property
    def reply_menu(self) -> ReplyKeyboardMarkup:
        """Геттер для нижней клавиатуры."""
        return self.__make_reply_keyboard()

    @property
    def inline_menu(self) -> InlineKeyboardMarkup:
        """Геттер для верхней клавиатуры."""
        return self.__make_inline_keyboard()

    @property
    def inline_stop_button(self) -> InlineKeyboardMarkup:
        """Геттер для остановки ввода с клавиатуры"""
        return self.__make_inline_stop_keyboard()  # Исправлено


Menu = MainKeyboardManager()
