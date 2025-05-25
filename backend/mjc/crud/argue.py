import uuid
from datetime import datetime

from sqlmodel import select, Session, func

from mjc.model.entity import ArguePost, Widget, Profile, Page, Class, \
        ClassStudentLink, ArguePostVote, ArguePostWatch, ClassTeacherLink, ArguePostStatus, \
        ArguePostComment, ArguePostAttachment, ArguePostFeedback, ArguePostFeedbackAttachment, \
        ClassTeachingAssistantLink
from mjc.model.schema.argue import ArguePostCreate, ArguePostUpdate, ArguePostCommentCreate, \
        ArguePostVoteCreate, ArguePostFeedbackCreate, ArguePostAttachmentCreate, ArguePostFeedbackAttachmentCreate, \
        ArguePostWatchCreate
from mjc.model.schema.user import UserInDB
from mjc.crud.assignment import get_submitted_assignment


def get_teacher_class_argues(db: Session, username: str) -> list[ArguePost]:
    """
    获取老师所在的班级的 argue
    :param db:
    :param username:
    :return:
    """
    stmt = select(ArguePost).join(ArguePost.widget).join(Widget.page).join(Page.class_) \
                            .join(ClassTeacherLink, Class.id == ClassTeacherLink.class_id) \
                            .where(ClassStudentLink.username == username)
    argues: list[ArguePost] = db.exec(stmt).all()
    return argues


def get_ta_class_argues(db: Session, username: str) -> list[ArguePost]:
    stmt = select(ArguePost).join(ArguePost.widget).join(Widget.page).join(Page.class_) \
        .join(ClassTeachingAssistantLink, Class.id == ClassTeachingAssistantLink.class_id) \
        .where(ClassTeachingAssistantLink.username == username)
    argues: list[ArguePost] = db.exec(stmt).all()
    return argues


def get_student_class_argues(db: Session, username: str) -> list[ArguePost]:
    """
    获取学生的 argue 广场
    """
    # 选择学生所在的 class 的 argue
    stmt = select(ArguePost).join(ArguePost.widget).join(Widget.page).join(Page.class_) \
                     .join(ClassStudentLink, Class.id == ClassStudentLink.class_id) \
                     .where(ClassStudentLink.username == username)
    argues: list[ArguePost] = db.exec(stmt).all()
    return argues


def get_argue(db: Session, argue_id: int) -> ArguePost:
    stmt = select(ArguePost).where(ArguePost.id == argue_id)
    argue = db.exec(stmt).first()
    return argue


def count_argue_votes(db: Session, argue_id: int) -> (int, int):
    stmt = select(func.count(ArguePostVote.id)).where(ArguePostVote.argue_post_id == argue_id) \
                                               .where(ArguePostVote.is_support == True)
    support = db.exec(stmt).first()
    stmt = select(func.count(ArguePostVote.id)).where(ArguePostVote.argue_post_id == argue_id) \
                                               .where(ArguePostVote.is_support == False)
    not_support = db.exec(stmt).first()
    return support, not_support


def count_argue_watch(db: Session, argue_id: int) -> int:
    stmt = select(func.count(ArguePostWatch.id)).where(ArguePostWatch.argue_post_id == argue_id) \
                                                .where(ArguePostWatch.is_deleted == False)
    watch = db.exec(stmt).first()
    return watch


def create_argue(db: Session, argue: ArguePostCreate, user: UserInDB) -> ArguePost:
    submission = get_submitted_assignment(db, argue.submitted_assignment_id)
    argue_post = ArguePost(
        widget_id=argue.widget_id,
        submitted_assignment_id=argue.submitted_assignment_id,
        title=argue.title,
        create_time=datetime.now(),
        update_time=datetime.now(),
        content=argue.content,
        status=ArguePostStatus.SUBMITTED,
        old_score=submission.feedback.score if submission and submission.feedback else 0,
        editor_username=user.username,
    )
    db.add(argue_post)
    db.commit()
    db.refresh(argue_post)
    return argue_post


def get_argue_attachment(db: Session, file_id: uuid.UUID) -> ArguePostAttachment:
    stmt = select(ArguePostAttachment).where(ArguePostAttachment.file_id == file_id) \
                                      .where(ArguePostAttachment.is_deleted == False)
    attach = db.exec(stmt).first()
    return attach


def create_argue_attachment(db: Session, attach: ArguePostAttachmentCreate) -> ArguePostAttachment:
    attach_entity = ArguePostAttachment(
        file_id=attach.file_id,
        argue_post_id=attach.argue_post_id
    )
    db.add(attach_entity)
    db.commit()
    db.refresh(attach_entity)
    return attach_entity


def delete_argue_attachment(db: Session, file_id: uuid.UUID):
    attach = get_argue_attachment(db, file_id)
    if attach:
        attach.is_deleted = True
        db.commit()
        db.refresh(attach)
    return attach


def update_argue(db: Session, argue: ArguePostUpdate) -> ArguePost:
    argue_post = get_argue(db, argue.id)
    if argue_post:
        argue_post.title = argue.title
        argue_post.content = argue.content
    db.commit()
    db.refresh(argue_post)
    return argue_post


def delete_argue(db: Session, argue_id: int) -> ArguePost:
    argue_post = get_argue(db, argue_id)
    if argue_post:
        argue_post.is_deleted = True
    db.commit()
    return argue_post


def count_argue_comment(db: Session, argue_id: int) -> int:
    stmt = select(func.count(ArguePostComment.id)).where(ArguePostComment.argue_post_id == argue_id)
    count = db.exec(stmt).first()
    return count


def create_comment(db: Session, comment: ArguePostCommentCreate, editor: UserInDB) -> ArguePostComment:
    cmt = ArguePostComment(
        argue_post_id=comment.argue_post_id,
        reply_to=comment.reply_to,
        content=comment.content,
        create_time=datetime.now(),
        editor_username=editor.username
    )
    db.add(cmt)
    db.commit()
    db.refresh(cmt)
    return cmt


def get_feedback_attachment(db: Session, file_id: uuid.UUID) -> ArguePostFeedbackAttachment:
    stmt = select(ArguePostFeedbackAttachment).where(ArguePostFeedback.file_id == file_id) \
                                              .where(ArguePostFeedbackAttachment.is_deleted == False)
    attach = db.exec(stmt).first()
    return attach


def create_feedback_attachment(db: Session, attach: ArguePostFeedbackAttachmentCreate) -> ArguePostFeedbackAttachment:
    attach_entity = ArguePostFeedbackAttachment(
        file_id=attach.file_id,
        argue_post_feedback_id=attach.argue_post_feedback_id
    )
    db.add(attach_entity)
    db.commit()
    db.refresh(attach_entity)
    return attach_entity


def delete_feedback_attachment(db: Session, file_id: uuid.UUID) -> ArguePostFeedbackAttachment:
    attach = get_feedback_attachment(db, file_id)
    if attach:
        attach.is_deleted = True
        db.commit()
        db.refresh(attach)
    return attach


def create_feedback(db: Session, feedback: ArguePostFeedbackCreate, marker: UserInDB) -> ArguePostFeedback:
    argue_post = get_argue(db, feedback.argue_post_id)
    submission_feedback = get_submitted_assignment(db, argue_post.submitted_assignment_id).feedback
    feedback_entity = ArguePostFeedback(
        argue_post_id=feedback.argue_post_id,
        content=feedback.content,
        score=feedback.score,
        create_time=datetime.now(),
        marker_username=marker.username,
    )
    db.add(feedback_entity)
    submission_feedback.score = submission_feedback.score
    db.commit()
    db.refresh(feedback_entity)
    return feedback_entity


def create_argue_vote(db: Session, argue: ArguePostVoteCreate, voter: UserInDB) -> ArguePostVote:
    argue_vote = ArguePostVote(
        argue_post_id=argue.argue_post_id,
        is_support=argue.is_support,
        voter_username=voter.username
    )
    db.add(argue_vote)
    db.commit()
    db.refresh(argue_vote)
    return argue_vote


def get_argue_watch(db: Session, argue_post_id: int, watcher: UserInDB) -> ArguePostWatch:
    stmt = select(ArguePostWatch).where(ArguePostWatch.argue_post_id == argue_post_id) \
                                 .where(ArguePostWatch.watcher_username == watcher.username) \
                                 .where(ArguePostWatch.is_deleted == False)
    watch = db.exec(stmt).first()
    return watch


def create_argue_watch(db: Session, watch: ArguePostWatchCreate, watcher: UserInDB) -> ArguePostWatch:
    argue_watch = ArguePostWatch(
        argue_post_id=watch.argue_post_id,
        watcher_username=watcher.username
    )
    db.add(argue_watch)
    db.commit()
    db.refresh(argue_watch)
    return argue_watch


def delete_argue_watch(db: Session, argue_post_id: int, watcher: UserInDB) -> ArguePostWatch:
    watch = get_argue_watch(db, argue_post_id, watcher)
    if watch:
        watch.is_deleted = True
    db.commit()
    db.refresh(watch)
    return watch