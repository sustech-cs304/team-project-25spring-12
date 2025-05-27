from fastapi import HTTPException
from sqlmodel import Session
from typing_extensions import Tuple

from mjc.model.schema.course import (ClassCreate, ClassUpdate, SemesterCreate,
                                     SemesterUpdate, Class, Semester, ClassCard,
                                     ClassUserEnroll, ClassUserUpdate, DDL, ClassUserRoleName)
from mjc.model.schema.common import File, Message
from mjc.model.schema.user import UserInDB
from mjc.crud import course as crud_course, user as crud_user
from mjc.model.entity.course import Class as ClassEntity, Semester as SemesterEntity, ClassRole, ClassUserLink
from mjc.model.entity.widget import WidgetType


def entity2cls(cls_entity: ClassEntity, role: str) -> Class:
    cls = Class(name=cls_entity.name,
                course_code=cls_entity.course_code,
                semester=cls_entity.semester.name,
                lecturer=cls_entity.lecturer,
                location=cls_entity.location,
                time=cls_entity.time,
                id=cls_entity.id,
                syllabus=File(
                    id=cls_entity.syllabus.id,
                    filename=cls_entity.syllabus.filename,
                    visibility=cls_entity.syllabus.visibility,
                    url=None
                ) if cls_entity.syllabus else None,
                role=ClassRole(role))
    return cls


def cls_user_2cls_card(cls_pair: Tuple[ClassEntity, ClassUserLink]) -> ClassCard:
    cls, link = cls_pair
    class_card = ClassCard(id=cls.id,
                           name=cls.name,
                           course_code=cls.course_code,
                           semester=cls.semester.name,
                           lecturer=cls.lecturer,
                           location=cls.location,
                           time=cls.time,
                           role=ClassRole(link.role))
    return class_card


def cls2cls_card(cls: ClassEntity) -> ClassCard:
    class_card = ClassCard(id=cls.id,
                           name=cls.name,
                           course_code=cls.course_code,
                           semester=cls.semester.name,
                           lecturer=cls.lecturer,
                           location=cls.location,
                           time=cls.time,
                           role=None)
    return class_card


def entity2semester(semester_entity: SemesterEntity) -> Semester:
    semester = Semester(id=semester_entity.id,
                        name=semester_entity.name,
                        start_time=semester_entity.start_time,
                        end_time=semester_entity.end_time)
    return semester


def entity2class_user_role(db: Session, link: ClassUserLink) -> ClassUserRoleName:
    return ClassUserRoleName(username=link.username,
                        name=crud_user.get_profile(db, link.username).name,
                        role=link.role)


def get_class(db: Session, cls_id: int) -> Class | None:
    cls_entity = crud_course.get_class(db, cls_id)
    if cls_entity is None:
        raise HTTPException(status_code=404, detail="Course not found")
    cls = entity2cls(cls_entity, '')
    return cls


def get_user_class_cards(db: Session, user: UserInDB) -> list[ClassCard] | None:
    cls_entities = crud_course.get_user_classes(db, user)
    return [cls_user_2cls_card(cls_entity) for cls_entity in cls_entities]


def create_class(db: Session, cls: ClassCreate) -> Class:
    cls_entity = crud_course.create_class(db, cls)
    if cls_entity is None:
        raise HTTPException(status_code=404, detail="Create class failed")
    cls = entity2cls(cls_entity, 'teacher')
    return cls


def update_class(db: Session, cls: ClassUpdate) -> Class:
    cls_entity = crud_course.update_class(db, cls)
    if cls_entity is None:
        raise HTTPException(status_code=404, detail="Update class failed")
    cls = entity2cls(cls_entity, 'teacher')
    return cls


def delete_class(db: Session, cls_id: int) -> Message:
    cls_entity = crud_course.delete_class(db, cls_id)
    if cls_entity:
        return Message(msg="Class deleted successfully")
    raise HTTPException(status_code=404, detail="Delete class failed")



def get_semesters(db: Session) -> list[Semester] | None:
    semester_entities = crud_course.get_semesters(db)
    if semester_entities is None:
        return None
    semesters = []
    for semester_entity in semester_entities:
        semester = entity2semester(semester_entity)
        semesters.append(semester)
    return semesters


def create_semester(db: Session, semester: SemesterCreate) -> Semester:
    semester_entity = crud_course.create_semester(db, semester)
    if semester_entity is None:
        raise HTTPException(status_code=404, detail="Create semester failed")
    semester = entity2semester(semester_entity)
    return semester


def update_semester(db: Session, semester: SemesterUpdate) -> Semester:
    semester_entity = crud_course.update_semester(db, semester)
    if semester_entity is None:
        raise HTTPException(status_code=404, detail="Update semester failed")
    semester = entity2semester(semester_entity)
    return semester


def delete_semester(db: Session, semester_id: int) -> Message:
    semester_entity = crud_course.delete_semester(db,semester_id)
    if semester_entity:
        return Message(msg="Semester deleted successfully")
    raise HTTPException(status_code=404, detail="Delete semester failed")


def get_user_class_role(db: Session, username: str, cls_id: int) -> ClassRole | None:
    link = crud_course.get_class_user_link(db, username, cls_id)
    if link:
        return link.role
    return None


def get_class_role(db:Session, cls_id: int) -> list[ClassUserRoleName] | None:
    links = crud_course.get_class_roles(db, cls_id)
    if links:
        return [entity2class_user_role(db, link) for link in links]


def enroll_class_users(db: Session, enroll: ClassUserEnroll) -> [ClassUserRoleName]:
    links = crud_course.enroll_class_users(db, enroll)
    users: [ClassUserRoleName] = []
    if links:
        users = [entity2class_user_role(db, link) for link in links]
    return users


def update_class_user(db: Session, class_user: ClassUserUpdate) -> ClassUserRoleName | None:
    link = crud_course.update_class_user(db, class_user)
    if link:
        return entity2class_user_role(db, link)


def unroll_class_user(db: Session, class_id: int, username: str) -> Message:
    crud_course.unroll_class_user(db, class_id, username)
    return Message(msg="success")


def get_ddl_calendar(db: Session, user: UserInDB) -> list[DDL]:
    classes = crud_course.get_student_classes(db, user)
    print(classes)
    ddls: list[DDL] = []
    if classes:
        for cls in classes:
            for page in cls.pages:
                for widget in page.widgets:
                    if widget.is_deleted == False and widget.type == WidgetType.assignment and widget.visible == True:
                        ddl=DDL(
                            class_id=cls.id,
                            class_name=cls.name,
                            course_code=cls.course_code,
                            page_id=page.id,
                            page_name=page.name,
                            widget_id=widget.id,
                            widget_title=widget.title,
                            ddl=widget.assignment_widget.ddl
                        )
                        ddls.append(ddl)
    return ddls


def get_semester_classes(db: Session, semester_id: int) -> list[ClassCard]:
    entities = crud_course.get_semester_classes(db, semester_id)
    return [cls2cls_card(entity) for entity in entities]
