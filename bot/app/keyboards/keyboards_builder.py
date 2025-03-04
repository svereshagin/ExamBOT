from pathlib import Path
from typing import Optional, Dict, Any, Callable, Tuple

import yaml
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class KeyboardBuilder:
    __base_yml_file: Path = Path(__file__).parent.joinpath("keyboards.yml")

    def __init__(self):
        self._keyboard_data: Optional[Dict[str, Any]] = self._read_yml_file()
        self._buttons = self._keyboard_data

    def _read_yml_file(self) -> Optional[Dict[str, Any]]:
        if self.__base_yml_file.exists():
            with open(self.__base_yml_file, "r", encoding="utf-8") as f:
                return yaml.load(f, Loader=yaml.FullLoader)
        else:
            raise FileNotFoundError(f"Файл {self.__base_yml_file} не найден.")

    def get_keyboard(self, mode: Tuple ) -> InlineKeyboardMarkup:
        """Создаёт клавиатуру на основе YAML-файла."""
        builder = InlineKeyboardBuilder()

        for text, callback_data in self._buttons[mode[0]][mode[1]].items():
            builder.button(text=text, callback_data=callback_data)

        builder.adjust(1)  # Одна кнопка в строке
        return builder.as_markup()
keyboard_builder = KeyboardBuilder()
# print(keyboard_builder.get_keyboard(mode=("startup_keyboard", "buttons")))
# print(keyboard_builder.get_keyboard(mode=("timer_options", "buttons")))