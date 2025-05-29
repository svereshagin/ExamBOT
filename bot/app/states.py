from aiogram.fsm.state import State, StatesGroup


class StartUpIK(StatesGroup):
    command_start_preparations = State()
    command_start_timer = State()
    command_get_reports = State()
    command_clear_db = State()
    command_docs = State()
