from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

import backend.mjc.model.schema.course
from backend.mjc.model.schema.course import SemesterCreate
from backend.mjc.model.schema.user import UserInDB
from backend.mjc.service import course as course_service
from backend.mjc.service import user as user_service
from backend.mjc.utils.database import SessionDep

router = APIRouter()


@router.get(path="/class/{class_id}", response_model=backend.mjc.model.schema.course.Class)
async def get_class(db: SessionDep, class_id: int):
    return course_service.get_class(db, class_id)


@router.get(path="/class/semester", response_model=list[backend.mjc.model.schema.course.Semester])
async def get_semester(db: SessionDep):
    return course_service.get_semesters(db)


@router.post(path="/class", response_model=backend.mjc.model.schema.course.Class)
async def create_class(db: SessionDep,
                       cls: backend.mjc.model.schema.course.ClassCreate,
                       current_user: UserInDB = Depends(user_service.get_current_user)
                       ):
    if current_user and current_user.is_admin:
        return course_service.create_class(db, cls)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")


@router.patch(path="/class", response_model=backend.mjc.model.schema.course.Class)
async def update_class(db: SessionDep,
                       cls: backend.mjc.model.schema.course.ClassUpdate,
                       current_user: UserInDB = Depends(user_service.get_current_user)):
    if current_user and current_user.is_admin:
        return course_service.update_class(db, cls)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")


@router.delete(path="/class/{class_id}", response_model=backend.mjc.model.schema.course.Class)
async def delete_class(db: SessionDep,
                       class_id: int,
                       current_user: UserInDB = Depends(user_service.get_current_user)):
    if current_user and current_user.is_admin:
        return course_service.delete_class(db, class_id)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")


@router.post(path="/class/semester", response_model=backend.mjc.model.schema.course.Semester)
async def create_semester(db: SessionDep,
                          semester: backend.mjc.model.schema.course.SemesterCreate,
                          current_user: UserInDB = Depends(user_service.get_current_user)):
    if current_user and current_user.is_admin:
        return course_service.create_semester(db, semester)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")


@router.patch(path="/class/semester", response_model=backend.mjc.model.schema.course.Semester)
async def update_semester(db: SessionDep,
                          semester: backend.mjc.model.schema.course.SemesterUpdate,
                          current_user: UserInDB = Depends(user_service.get_current_user)):
    if current_user and current_user.is_admin:
        return course_service.update_semester(db, semester)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")


@router.delete(path="/class/semester/{semester_id}", response_model=backend.mjc.model.schema.course.Semester)
async def delete_semester(db: SessionDep,
                          semester_id: int,
                          current_user: UserInDB = Depends(user_service.get_current_user)):
    if current_user and current_user.is_admin:
        return course_service.delete_semester(db, semester_id)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
