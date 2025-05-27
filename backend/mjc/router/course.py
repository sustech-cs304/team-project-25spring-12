from fastapi import APIRouter, Depends, HTTPException, status

from mjc.model.schema.common import Message
from mjc.model.schema.assignment import DDL
from mjc.model.schema.course import Class, Semester, ClassCreate, ClassUpdate, SemesterCreate, SemesterUpdate, ClassCard,\
    ClassUserEnroll, ClassUserRoleName, ClassUserUpdate
from mjc.model.schema.user import UserInDB
from mjc.model.schema.widget import AssignmentWidget
from mjc.service import course as course_service, widget as widget_service
from mjc.permission import course as course_permission, common as common_permission
from mjc.service.user import get_current_user
from mjc.utils.database import SessionDep

router = APIRouter()


@router.get(path='/class', response_model=list[ClassCard])
async def get_classes(db: SessionDep, current_user: UserInDB = Depends(get_current_user)):
    return course_service.get_user_class_cards(db, current_user)


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


@router.post(path="/class/semester", response_model=Semester,
             dependencies=[Depends(course_permission.verify_class_create)])
async def create_semester(db: SessionDep,
                          semester: SemesterCreate,
                          current_user: UserInDB = Depends(get_current_user)):
    if current_user and current_user.is_admin:
        return course_service.create_semester(db, semester)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")


@router.patch(path="/class/semester", response_model=Semester,
              dependencies=[Depends(common_permission.verify_admin)])
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


@router.post(path="/class/user", response_model=list[ClassUserRoleName])
async def create_user_roll(db: SessionDep, enroll: ClassUserEnroll):
    return course_service.enroll_class_users(db, enroll)


@router.patch(path="/class/user", response_model=ClassUserRoleName)
async def update_user_roll(db: SessionDep, update: ClassUserUpdate):
    return course_service.update_class_user(db, update)


@router.delete(path="/class/{cls_id}/user/{username}", response_model=Message)
async def delete_user_roll(db: SessionDep, cls_id: int, username: str):
    return course_service.unroll_class_user(db, cls_id, username)


@router.get(path="/class/{class_id}/user", response_model=list[ClassUserRoleName])
async def get_class_user(db: SessionDep, class_id: int):
    return course_service.get_class_role(db, class_id)


@router.get(path="/ddl", response_model=list[DDL])
async def get_ddl(db: SessionDep, current_user: UserInDB = Depends(get_current_user)):
    return course_service.get_ddl_calendar(db, current_user)


@router.get(path="/class/{clas_id}/assignments",
            response_model=list[AssignmentWidget])
def get_class_assignments(db: SessionDep, class_id: int,
                          current_user: UserInDB = Depends(get_current_user)) -> list[AssignmentWidget]:
    return widget_service.get_class_assignments(db, class_id, current_user)


@router.get(path="/admin/semester/{semester_id}", response_model=list[ClassCard])
def get_semester_classes(db: SessionDep, semester_id: int) -> list[ClassCard]:
    return course_service.get_semester_classes(db, semester_id)
