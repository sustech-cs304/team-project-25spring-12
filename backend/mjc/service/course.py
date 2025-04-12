from fastapi import HTTPException
from sqlmodel import Session

from backend.mjc.model.schema.course import (ClassCreate, ClassUpdate, SemesterCreate,
                                             SemesterUpdate, Class, Semester, ClassCard,
                                             ClassUserEnroll, ClassUserUpdate)
from backend.mjc.model.schema.common import File, Message
from backend.mjc.model.schema.user import UserInDB, Profile
from backend.mjc.crud import course as crud_course
from backend.mjc.model.entity import Class as ClassEntity, Semester as SemesterEntity, ClassRole


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
                    file_name=cls_entity.syllabus.filename,
                    visibility=cls_entity.syllabus.visibility,
                    url=None
                ) if cls_entity.syllabus else None,
                role=ClassRole(role))
    return cls


def cls2cls_card(cls: Class) -> ClassCard:
    class_card = ClassCard.model_validate(cls)
    return class_card


def entity2semester(semester_entity: SemesterEntity) -> Semester:
    semester = Semester(id=semester_entity.id,
                        name=semester_entity.name,
                        start_time=semester_entity.start_time,
                        end_time=semester_entity.end_time)
    return semester


def get_class(db: Session, cls_id: int) -> Class | None:
    cls_entity = crud_course.get_class(db, cls_id)
    if cls_entity is None:
        raise HTTPException(status_code=404, detail="Course not found")
    cls = entity2cls(cls_entity, '')
    return cls


def get_student_classes(db: Session, user: UserInDB) -> list[Class] | None:
    cls_entities = crud_course.get_student_classes(db, user)
    if cls_entities is None:
        return None
    classes = []
    for cls_entity in cls_entities:
        classes.append(entity2cls(cls_entity, 'student'))
    return classes


def get_teacher_classes(db: Session, user: UserInDB) -> list[Class] | None:
    cls_entities = crud_course.get_teacher_classes(db,user)
    if cls_entities is None:
        return None
    classes = []
    for cls_entity in cls_entities:
        classes.append(entity2cls(cls_entity, 'teacher'))
    return classes


def get_ta_classes(db: Session, user: UserInDB) -> list[Class] | None:
    cls_entities = crud_course.get_ta_classes(db,user)
    if cls_entities is None:
        return None
    classes = []
    for cls_entity in cls_entities:
        classes.append(entity2cls(cls_entity, 'ta'))
    return classes


def get_student_class_cards(db: Session, user: UserInDB) -> list[ClassCard] | None:
    classes = get_student_classes(db, user)
    if classes is None:
        return None
    class_cards = []
    for cls in classes:
        class_card = cls2cls_card(cls)
        class_cards.append(class_card)
    return class_cards


def get_teacher_class_cards(db: Session, user: UserInDB) -> list[ClassCard] | None:
    classes = get_teacher_classes(db, user)
    if classes is None:
        return None
    class_cards = []
    for cls in classes:
        class_card = cls2cls_card(cls)
        class_cards.append(class_card)
    return class_cards


def get_ta_class_cards(db: Session, user: UserInDB) -> list[ClassCard] | None:
    classes = get_ta_classes(db, user)
    if classes is None:
        return None
    class_cards = []
    for cls in classes:
        class_card = cls2cls_card(cls)
        class_cards.append(class_card)
    return class_cards


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


def get_user_class_role(db: Session, username: str, cls_id: int) -> ClassRole:
    return crud_course.get_user_class_role(db, username, cls_id)


def enroll_class_users(db: Session, enroll: ClassUserEnroll) -> Class:
    return crud_course.enroll_class_users(db, enroll)


def update_class_user(db: Session, class_user: ClassUserUpdate) -> Class:
    return crud_course.update_class_user(db, class_user)


def unroll_class_user(db: Session, class_id: int, username: str) -> Class:
    return crud_course.unroll_class_user(db, class_id, username)