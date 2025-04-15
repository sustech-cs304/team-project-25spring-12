from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from mjc.model.schema.common import Message
from mjc.model.schema.course import Class, Semester, ClassCreate, ClassUpdate, SemesterCreate, SemesterUpdate, ClassUserEnroll
from mjc.model.schema.assignment import DDL
from mjc.model.schema.user import UserInDB, Profile
from mjc.service import course as course_service
from mjc.service import user as user_service
from mjc.permission import course as course_permission
from mjc.service.user import get_current_user
from mjc.utils.database import SessionDep

router = APIRouter()


@router.get(path="/class/semester", response_model=list[Semester],
            dependencies=[Depends(get_current_user)])
async def get_semester(db: SessionDep):
    return course_service.get_semesters(db)


@router.get(path="/class/{class_id}", response_model=Class,
            dependencies=[Depends(course_permission.verify_class_get)])
async def get_class(db: SessionDep, class_id: int):
    return course_service.get_class(db, class_id)


@router.post(path="/class", response_model=Class,
             dependencies=[Depends(course_permission.verify_class_create)])
async def create_class(db: SessionDep, cls: ClassCreate,
                       current_user: UserInDB = Depends(get_current_user)):
    if current_user and current_user.is_admin:
        return course_service.create_class(db, cls)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")


@router.patch(path="/class", response_model=Class,
              dependencies=[Depends(course_permission.verify_class_update)])
async def update_class(db: SessionDep, cls: ClassUpdate,
                       current_user: UserInDB = Depends(get_current_user)):
    if current_user and current_user.is_admin:
        return course_service.update_class(db, cls)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")


@router.delete(path="/class/{class_id}", response_model=Class,
               dependencies=[Depends(course_permission.verify_class_delete)])
async def delete_class(db: SessionDep,
                       class_id: int,
                       current_user: UserInDB = Depends(get_current_user)):
    if current_user and current_user.is_admin:
        return course_service.delete_class(db, class_id)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")


@router.post(path="/class/semester", response_model=Semester)
async def create_semester(db: SessionDep,
                          semester: SemesterCreate,
                          current_user: UserInDB = Depends(get_current_user)):
    if current_user and current_user.is_admin:
        return course_service.create_semester(db, semester)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")


@router.patch(path="/class/semester", response_model=Semester)
async def update_semester(db: SessionDep,
                          semester: SemesterUpdate,
                          current_user: UserInDB = Depends(get_current_user)):
    if current_user and current_user.is_admin:
        return course_service.update_semester(db, semester)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")


@router.delete(path="/class/semester/{semester_id}", response_model=Message)
async def delete_semester(db: SessionDep,
                          semester_id: int,
                          current_user: UserInDB = Depends(get_current_user)):
    if current_user and current_user.is_admin:
        return course_service.delete_semester(db, semester_id)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")


@router.post(path="/class/user", response_model=list[Profile])
async def create_user_roll(db: SessionDep, enroll: ClassUserEnroll):
    return course_service.enroll_class_users(db, enroll)


@router.get(path="/class/{class_id}/user")
async def get_class_user(db: SessionDep, class_id: int):
    # TODO:
    pass


@router.get(path="/ddl", response_model=list[DDL])
async def get_ddl(db: SessionDep, current_user: UserInDB = Depends(get_current_user)):
    return course_service.get_ddl_calendar(db, current_user)
