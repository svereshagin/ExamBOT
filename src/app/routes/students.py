# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.database import SessionLocal
# from app.services.student_service import get_all_students, set_student_mark
# from app.schemas.student import StudentSchema, MarkInput
# from typing import List
#
# router = APIRouter()
#
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#
# @router.get("/students", response_model=List[StudentSchema])
# async def fetch_students(db: Session = Depends(get_db)):
#     return get_all_students(db)
#
# @router.post("/students/{student_id}/mark")
# async def update_mark(student_id: int, mark_input: MarkInput, db: Session = Depends(get_db)):
#     student = set_student_mark(db, student_id, mark_input.mark)
#     if not student:
#         raise HTTPException(status_code=404, detail="Студент не найден")
#     return {"message": "Оценка обновлена"}