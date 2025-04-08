from sqlmodel import Session, select

from ..model.schema.course import ClassCreate, ClassUpdate, SemesterCreate, SemesterUpdate
from ..model.entity import Class, Semester, Profile, ClassStudentLink
from ..model.schema.user import UserInDB


def get_class(db: Session, class_id: int) -> Class:
    stmt = select(Class).where(Class.id == class_id).where(Class.is_deleted == False)
    cls_entity = db.exec(stmt).first()
    return cls_entity


def get_student_classes(db: Session, user: UserInDB) -> list[Class]:
    stmt = select(Profile).where(Profile.username == user.username)
    student: Profile = db.exec(stmt).first()
    return [cls for cls in student.student_classes if cls.is_deleted == False]


def get_teacher_classes(db: Session, user: UserInDB) -> list[Class]:
    stmt = select(Profile).where(Profile.username == user.username)
    teacher: Profile = db.exec(stmt).first()
    return [cls for cls in teacher.teacher_classes if cls.is_deleted == False]


def get_ta_classes(db: Session, user: UserInDB) -> list[Class]:
    stmt = select(Class).where(Profile.username == user.username)
    ta: Profile = db.exec(stmt).first()
    return [cls for cls in ta.teaching_assistant_classes if cls.is_deleted == False]


def get_semester_classes(db: Session, semester_id: int) -> list[Class]:
    stmt = select(Class).where(Class.semester_id == semester_id).where(Class.is_deleted == False)
    cls_entities = db.exec(stmt).all()
    return cls_entities


def get_semesters(db: Session) -> list[Semester]:
    stmt = select(Semester).where(Semester.is_deleted == False)
    sem_entities = db.exec(stmt).all()
    return sem_entities


def create_class(db: Session, cls: ClassCreate) -> Class:
    cls_entity = Class(
        name=cls.name,
        course_code=cls.course_code,
        semester_id=cls.semester_id,
        lecturer=cls.lecturer,
        location=cls.location,
        time=cls.time,
        syllabus_id=cls.syllabus.id
    )
    db.add(cls_entity)

    if cls.template_id:
        # TODO: 当存在课程模板的时候为课程添加默认结构
        pass

    return cls_entity


def update_class(db: Session, cls: ClassUpdate) -> Class:
    stmt = select(Class).where(Class.id == cls.id).where(Class.is_deleted == False)
    cls_entity = db.exec(stmt).first()
    if cls_entity:
        cls_entity.name = cls.name
        cls_entity.course_code = cls.course_code
        cls_entity.semester_id = cls.semester_id
        cls_entity.lecturer = cls.lecturer
        cls_entity.location = cls.location
        cls_entity.time = cls.time
        cls_entity.syllabus_id = cls.syllabus.id
    return cls_entity


def delete_class(db: Session, cls: Class) -> Class:
    stmt = select(Class).where(Class.id == cls.id).where(Class.is_deleted == False)
    cls_entity = db.exec(stmt).first()
    if cls_entity:
        cls_entity.is_deleted = True
    return cls_entity


def create_semester(db: Session, semester: SemesterCreate) -> Semester:
    semester_entity = Semester(
        name=semester.name,
        start_time=semester.start_time,
        end_time=semester.end_time,
    )
    db.add(semester_entity)
    return semester_entity


def update_semester(db: Session, semester: SemesterUpdate) -> Semester:
    stmt = select(Semester).where(Semester.id == semester.id).where(Semester.is_deleted == False)
    semester_entity = db.exec(stmt).first()
    if semester_entity:
        semester_entity.name = semester.name
        semester_entity.start_time = semester.start_time
        semester_entity.end_time = semester.end_time
    return semester_entity


def delete_semester(db: Session, semester_id: int) -> Semester:
    stmt = select(Semester).where(Semester.id == semester_id).where(Semester.is_deleted == False)
    semester_entity = db.exec(stmt).first()
    if semester_entity:
        semester_entity.is_deleted = True
    return semester_entity