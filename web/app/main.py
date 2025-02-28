from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

app = FastAPI()

# Корневая директория проекта
BASE_DIR = Path(__file__).parent.parent.parent.resolve()

# Подключение статических файлов
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


# Отображение HTML-страницы
@app.get("/", response_class=HTMLResponse)
async def get_students_page():
    html_path = (BASE_DIR / "templates" / "students.html").read_text(encoding="utf-8")
    return HTMLResponse(content=html_path)


# TODO запуск -->>>     uvicorn main:app --reload
# todo /project/code/web/app
