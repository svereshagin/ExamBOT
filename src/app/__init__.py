from fastapi import FastAPI

app = FastAPI()


@app.get("students")
async def get_students():
    """хендлер для получения всех студентов на странице"""
    return await get_all_students()

@app.post("/students/id")
async def add_mark():
    """хендлер для проставления оценок студентам"""
    return