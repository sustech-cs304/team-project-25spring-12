from sqlmodel import Session, select

from mjc.model.schema.course import ClassCreate, ClassUpdate, SemesterCreate, SemesterUpdate
from mjc.model.entity import Class, Semester, Profile, \
                                     ClassStudentLink, ClassTeacherLink, ClassTeachingAssistantLink, ClassRole
from mjc.model.schema.user import UserInDB
from mjc.crud.user import get_profile
from mjc.model.schema.course import ClassUserEnroll, ClassUserUpdate


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


def get_user_class_role(db: Session, username: str, cls_id: int) -> ClassRole:
    stmt = select(ClassStudentLink).where(ClassStudentLink.class_id == cls_id) \
                                   .where(ClassStudentLink.username == username)
    if db.exec(stmt).first():
        return ClassRole.STUDENT
    stmt = select(ClassTeacherLink).where(ClassTeacherLink.class_id == cls_id) \
                                   .where(ClassTeacherLink.username == username)
    if db.exec(stmt).first():
        return ClassRole.TEACHER
    stmt = select(ClassTeachingAssistantLink).where(ClassTeachingAssistantLink.class_id == cls_id) \
                                             .where(ClassTeachingAssistantLink.username == username)
    if db.exec(stmt).first():
        return ClassRole.TA


def enroll_class_users(db: Session, assign: ClassUserEnroll) -> Class:
    cls = get_class(db, assign.class_id)
    if cls:
        for username in assign.usernames:
            user = get_profile(db, username)
            if user:
                if assign.role is ClassRole.STUDENT:
                    cls.students.append(user)
                elif assign.role is ClassRole.TEACHER:
                    cls.teachers.append(user)
                elif assign.role is ClassRole.TA:
                    cls.teaching_assistants.append(user)
        db.refresh(cls)
    return cls


def update_class_user(db: Session, assign: ClassUserUpdate) -> Class:
    cls = get_class(db, assign.class_id)
    if cls:
        user = get_profile(db, assign.username)
        if user:
            role = get_user_class_role(db, user.username, assign.class_id)
            if role is ClassRole.STUDENT:
                cls.students.remove(user)
            elif role is ClassRole.TEACHER:
                cls.teachers.remove(user)
            elif role is ClassRole.TA:
                cls.teaching_assistants.remove(user)
            if assign.role is ClassRole.STUDENT:
                cls.students.append(user)
            if assign.role is ClassRole.TEACHER:
                cls.teachers.append(user)
            if assign.role is ClassRole.TA:
                cls.teaching_assistants.append(user)
            db.refresh(cls)
    return cls


def unroll_class_user(db: Session, class_id: int, username: str) -> Class:
    cls = get_class(db, class_id)
    if cls:
        user = get_profile(db, username)
        if user:
            role = get_user_class_role(db, user.username, class_id)
            if role == ClassRole.STUDENT:
                if role == ClassRole.STUDENT:
                    cls.students.remove(user)
                elif role == ClassRole.TEACHER:
                    cls.teachers.remove(user)
                elif role == ClassRole.TA:
                    cls.teaching_assistants.remove(user)
        db.refresh(cls)
    return cls