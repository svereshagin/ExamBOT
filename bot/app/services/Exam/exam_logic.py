import time
from pydantic import BaseModel
from time_constants import *
from aiogram import Bot


class TimerData(BaseModel):
    # TODO состряпать новый тип для разбивки Timer и Timer Data
    __base_time_in_sec: int = 90 * 60

    def __init__(self, mode=None, theor_time: int = None, practice_time: int = None):
        self.mode = mode
        # TODO сделать валидацию типов через
        if self.mode:
            if self.mode == "standart":
                pass
                # TODO my logic
            elif self.mode == "special":
                pass
                # TODO special experience like 1 student = 15 mins or more.
        self.theor_time = theor_time


class Timer:
    __base_time_in_sec: int = 90 * 60
    __TEN_MINUTES: int = 10 * 60  # 10 * 60
    __FIVE_MINUTES: int = 5 * 60
    __THIRTEEN_MINUTES: int = 13 * 60
    __TIME_HAS_PASSED: int = 15 * 60
    __EXAM_TIME: bool = False

    def __init__(
        self, theor_time: int = 0, practice_time: int = 0, students_quantity: int = 0
    ):
        if self.validate(theor_time):
            self.__base_time_in_sec = theor_time
        if self.validate(practice_time):
            self.__base_time_in_sec += practice_time
        if self.__base_time_in_sec > 100:
            self.__base_time_in_sec = 100
        self.given_time_per_student = self.__base_time_in_sec / students_quantity

    def validate(self, time: int) -> bool:
        return time > 0 and time <= self.__base_time_in_sec

    def set_timer(self, students: list, bot: Bot, message):
        """
        Устанавливаем время экзамена
        Устанавливаем текущий id студента(будет итерация по списку т.е от 0 идём)
        Пока счётчик работает, в начале отсылаем предвещающие начало экзамена сообщения
        Далее, когда время закончилось и мы установили переменную в фазу "да"
        """
        timers_time = self.__base_time_in_sec
        while timers_time > 0:
            if self.__EXAM_TIME:
                students_id_counter = 0
                refresh_time: int = self.given_time_per_student
                bot.send_message(
                    message.from_chad.id,
                    f"Текущий участник {students[students_id_counter]}",
                )
                # реализовать отправку сообщения
                while self.given_time_per_student:
                    self.given_time_per_student -= 1
                    timers_time -= 1
                    time.sleep(1)
                self.given_time_per_student = refresh_time
                students_id_counter += 1

            notification = self.notify(timers_time)
            if notification:
                print(notification)  # change to bot notification
            timers_time -= 1
            time.sleep(1)
            # получает следующего студента из БД, увеличивает счётчик id на +1

    def ten_mins_passed(self, time: int):
        return True if time + self.__TEN_MINUTES == self.__base_time_in_sec else False

    def five_mins_passed(self, time: int):
        return True if time + self.__FIVE_MINUTES == self.__base_time_in_sec else False

    def thirteen_mins_passed(self, time: int):
        return (
            True if time + self.__THIRTEEN_MINUTES == self.__base_time_in_sec else False
        )

    def time_has_passed(self, time: int):
        return (
            True if time + self.__TIME_HAS_PASSED == self.__base_time_in_sec else False
        )

    def notify(self, time_sec: int):
        if self.ten_mins_passed(time_sec):
            return constant_text_ten_mins
        elif self.five_mins_passed(time_sec):
            return constant_text_five_mins
        elif self.thirteen_mins_passed(time_sec):
            return constant_text_thirteen_mins
        elif self.time_has_passed(time_sec):
            self.EXAM_TIME = True
            return constant_text_time_has_passed


Timer().set_timer()
