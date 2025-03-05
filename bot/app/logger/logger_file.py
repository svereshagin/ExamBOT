import logging
import os
from pathlib import Path


def setup_logger(level=logging.INFO):
    """Настройка логгера с использованием имени файла модуля."""
    base_path = Path(__file__).absolute().parents[2]  # будет на уровне bot
    # Получаем имя текущего модуля без расширения, формируем .log формат
    path_to_file: str = Path(__file__).name[:-3] + ".log"
    log_dir = "logger_info"
    # Создаем директорию для логов, если она не существует
    path_to_logging_dir: Path = base_path.joinpath(log_dir)
    path_to_logging_dir.mkdir(parents=True, exist_ok=True)  # создание директории
    path_to_logging_file: Path = path_to_logging_dir.joinpath(
        path_to_file
    )  # создании файла
    # Создаем логгер
    path_to_logging_file.touch(exist_ok=True)

    path_to_logging_file: str = str(path_to_logging_file)
    logger = logging.getLogger(path_to_logging_file)
    logger.setLevel(level)

    # Создаем обработчик для записи логов в файл
    file_handler = logging.FileHandler(path_to_logging_file)
    file_handler.setLevel(level)

    # Создаем обработчик для вывода логов на консоль
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


logger = setup_logger()
