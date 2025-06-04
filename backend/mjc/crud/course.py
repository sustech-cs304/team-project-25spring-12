from sqlmodel import Session, select

from mjc.model.schema.course import ClassCreate, ClassUpdate, SemesterCreate, SemesterUpdate
from mjc.model.entity.course import Class, Semester, ClassUserLink, ClassRole
from mjc.model.schema.user import UserInDB
from mjc.model.schema.course import ClassUserEnroll, ClassUserUpdate


def get_class(db: Session, class_id: int) -> Class:
    stmt = select(Class).where(Class.id == class_id).where(Class.is_deleted == False)
    cls_entity = db.exec(stmt).first()
    return cls_entity


def get_user_classes(db: Session, user: UserInDB) ->list[Class]:
    stmt = select(Class, ClassUserLink).join(ClassUserLink, Class.id == ClassUserLink.class_id) \
                        .where(ClassUserLink.username == user.username)
    classes: list[Class] = db.exec(stmt).all()
    return classes


def get_student_classes(db: Session, user: UserInDB) -> list[Class]:
    stmt = select(Class).join(ClassUserLink, Class.id == ClassUserLink.class_id) \
                        .where(ClassUserLink.username == user.username) \
                        .where(ClassUserLink.role == ClassRole.STUDENT)
    classes: list[Class] = db.exec(stmt).all()
    return classes


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
        syllabus_id=cls.syllabus.id if cls.syllabus else None
    )
    db.add(cls_entity)

    if cls.template_id:
        # TODO: 当存在课程模板的时候为课程添加默认结构
        pass

    db.commit()
    db.refresh(cls_entity)
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
        cls_entity.syllabus_id = cls.syllabus.id if cls.syllabus else None
    db.commit()
    return cls_entity


def delete_class(db: Session, cls_id: int) -> Class:
    stmt = select(Class).where(Class.id == cls_id).where(Class.is_deleted == False)
    cls_entity = db.exec(stmt).first()
    if cls_entity:
        cls_entity.is_deleted = True
    db.commit()
    return cls_entity


def create_semester(db: Session, semester: SemesterCreate) -> Semester:
    semester_entity = Semester(
        name=semester.name,
        start_time=semester.start_time,
        end_time=semester.end_time,
    )
    db.add(semester_entity)
    db.commit()
    db.refresh(semester_entity)
    return semester_entity


def update_semester(db: Session, semester: SemesterUpdate) -> Semester:
    stmt = select(Semester).where(Semester.id == semester.id).where(Semester.is_deleted == False)
    semester_entity = db.exec(stmt).first()
    if semester_entity:
        semester_entity.name = semester.name
        semester_entity.start_time = semester.start_time
        semester_entity.end_time = semester.end_time
    db.commit()
    return semester_entity


def delete_semester(db: Session, semester_id: int) -> Semester:
    stmt = select(Semester).where(Semester.id == semester_id).where(Semester.is_deleted == False)
    semester_entity = db.exec(stmt).first()
    if semester_entity:
        semester_entity.is_deleted = True
    db.commit()
    return semester_entity


def get_class_user_link(db: Session, username: str, cls_id: int) -> ClassUserLink:
    stmt = select(ClassUserLink).where(ClassUserLink.username == username).where(ClassUserLink.class_id == cls_id)
    link = db.exec(stmt).first()
    return link


def get_class_roles(db: Session, cls_id: int) -> list[ClassUserLink]:
    stmt = select(ClassUserLink).where(ClassUserLink.class_id == cls_id)
    links = db.exec(stmt).all()
    return links


def enroll_class_users(db: Session, assign: ClassUserEnroll) -> list[ClassUserLink]:
    links: list[ClassUserLink] = [ClassUserLink(username=username, class_id=assign.class_id, role=assign.role)
                                  for username in assign.usernames]
    db.add_all(links)
    db.commit()
    return links


def update_class_user(db: Session, assign: ClassUserUpdate) -> ClassUserLink:
    stmt = select(ClassUserLink).where(ClassUserLink.username == assign.username) \
                                .where(ClassUserLink.class_id == assign.class_id)
    link: ClassUserLink = db.exec(stmt).first()
    if link:
        link.role = assign.role
    db.commit()
    return link


def unroll_class_user(db: Session, class_id: int, username: str):
    link = get_class_user_link(db, username, class_id)
    if link:
        db.delete(link)
    db.commit()