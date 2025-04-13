import uuid

from sqlmodel import Session
from fastapi import HTTPException

from backend.mjc.crud import argue as crud_argue
from backend.mjc.model.schema.common import File, Message
from backend.mjc.model.schema.widget import AssignmentWidget
from backend.mjc.model.schema.user import UserInDB, Profile
from backend.mjc.model.schema.argue import ArguePostCard, ArguePost, ArguePostComment, ArguePostFeedback, \
    ArguePostUpdate, ArguePostVoteCreate, ArguePostAttachmentCreate, ArguePostFeedbackCreate, \
    ArguePostFeedbackAttachmentCreate, ArguePostCreate
from backend.mjc.model.schema.assignment import SubmittedAssignment, Feedback
from backend.mjc.model.entity import ArguePostAttachment, ArguePostFeedbackAttachment, WidgetAttachment, \
    SubmittedAssignmentAttachment, ArguePost as ArguePostEntity
from backend.mjc.crud.argue import count_argue_votes
from backend.mjc.model.schema.argue import ArguePostCommentCreate, ArguePostWatchCreate
from backend.mjc.service.assignment import entity2feedback


def argue2comments(argue: ArguePostEntity) -> list[ArguePostComment]:
    comments = [ArguePostComment(
                    **comment.model_dump(),
                    editor=Profile.model_validate(comment.editor.model_dump())
                ) for comment in argue.comments]
    return comments


def argue2assignment(argue: ArguePostEntity) -> AssignmentWidget:
    assignment = AssignmentWidget(
        id=argue.widget.id,
        title=argue.widget.title,
        content=argue.widget.content,
        attachments=attachments2files(argue.widget.attachments),
        submitted_assignment=[
            SubmittedAssignment(
                id=argue.submitted_assignment_id,
                content=argue.submitted_assignment.content,
                attachments=attachments2files(argue.submitted_assignment.attachments),
                code=argue.submitted_assignment.code,
                submitted_time=argue.submitted_assignment.create_time,
                feedback=entity2feedback(None, argue.submitted_assignment.feedback)
            )
        ],
        index=argue.widget.index,
        visible=argue.widget.visible,
        type=argue.widget.type,
        submit_types=argue.widget.assignment_widget.submit_types,
        status=' ',  # TODO: 批改状态
        ddl=argue.widget.assignment_widget.ddl,
        max_score=argue.widget.assignment_widget.max_score,
        create_time=argue.widget.create_time,
        update_time=argue.widget.update_time,
        editor=Profile.model_validate(argue.widget.editor.model_dump()),
    )
    return assignment


def argue2feedback(argue: ArguePostEntity) -> ArguePostFeedback:
    feedback = None
    if argue.feedback:
        feedback = ArguePostFeedback(
            id=argue.id,
            argue_post_id=argue.id,
            content=argue.feedback.content,
            score=argue.feedback.score,
            marker=Profile.model_validate(argue.feedback.marker.model_dump()),
            attachments=attachments2files(argue.attachments)
        )
    return feedback


def attachments2files(attachments: list[ArguePostAttachment |
                                        ArguePostFeedbackAttachment |
                                        WidgetAttachment |
                                        SubmittedAssignmentAttachment]) -> list[File]:
    files: list[File] = []
    for attach in attachments:
        if not attach.is_deleted:
            files.append(File.model_validate(attach.file.model_dump()))
    return files


def get_argues(db: Session, user: UserInDB) -> list[ArguePostCard]:
    argues = []
    student_argues = crud_argue.get_student_class_argues(db, user.username)
    teacher_argues = crud_argue.get_teacher_class_argues(db, user.username)
    ta_argues = crud_argue.get_ta_class_argues(db, user.username)
    argues.extend(student_argues + teacher_argues + ta_argues)

    cards: list[ArguePostCard] = []
    for argue in argues:
        support, not_support = count_argue_votes(db, argue.id)
        cards.append(ArguePostCard(
            id=argue.id,
            widget_id=argue.widget_id,
            submitted_assignment_id=argue.submitted_assignment_id,
            title=argue.title,
            content=argue.content,
            create_time=argue.create_time,
            update_time=argue.update_time,
            watch=crud_argue.count_argue_watch(db, argue.id),
            support=support,
            not_support=not_support,
            comments=crud_argue.count_argue_comment(db, argue.id),
            editor=Profile.model_validate(argue.editor.model_dump()),
            status=argue.status,
        ))
    return cards


def get_argue(db: Session, argue_id: int) -> ArguePost:
    argue = crud_argue.get_argue(db, argue_id)
    if argue is None:
        raise HTTPException(status_code=404, detail="Argue not found")
    support, not_support = count_argue_votes(db, argue.id)
    post = ArguePost(
        id=argue.id,
        widget_id=argue.widget_id,
        submitted_assignment_id=argue.submitted_assignment_id,
        title=argue.title,
        content=argue.content,
        create_time=argue.create_time,
        update_time=argue.update_time,
        watch=crud_argue.count_argue_watch(db, argue.id),
        support=support,
        not_support=not_support,
        comments=argue2comments(argue),
        feedback=argue2feedback(argue),
        editor=Profile.model_validate(argue.editor.model_dump()),
        status=argue.status,
        attachments=attachments2files(argue.attachments),
        old_score=argue.old_score,
        assignment=argue2assignment(argue)
    )
    return post


def create_argue(db: Session, argue: ArguePostCreate, user: UserInDB) -> ArguePost:
    argue_post = crud_argue.create_argue(db, argue, user)
    if argue_post is None:
        raise HTTPException(status_code=400, detail="Create argue failed")
    return get_argue(db, argue_post.id)


def update_argue(db: Session, argue: ArguePostUpdate) -> ArguePost:
    argue_post = crud_argue.get_argue(db, argue.id)
    if argue_post is None:
        raise HTTPException(status_code=404, detail="Argue not found")
    crud_argue.update_argue(db, argue)
    return get_argue(db, argue.id)


def delete_argue(db: Session, argue_id: int) -> Message:
    argue = crud_argue.get_argue(db, argue_id)
    if argue is None:
        raise HTTPException(status_code=404, detail="Argue not found")
    crud_argue.delete_argue(db, argue_id)
    return Message(msg='Success')


def create_argue_comment(db: Session, comment: ArguePostCommentCreate, user: UserInDB) -> ArguePostComment:
    cmt_entity = crud_argue.create_comment(db, comment, user)
    if cmt_entity is None:
        raise HTTPException(status_code=400, detail="Create comment failed")
    cmt_schema = ArguePostComment(**cmt_entity.model_dump(),
                                  editor=Profile.model_validate(cmt_entity.editor.model_dump()))
    return cmt_schema


def create_argue_watch(db: Session, watch: ArguePostWatchCreate, user: UserInDB) -> Message:
    if crud_argue.get_argue_watch(db, watch.argue_post_id, user):
        raise HTTPException(status_code=400, detail="Watch already exists")
    watch_entity = crud_argue.create_argue_watch(db, watch, user)
    if watch_entity is None:
        raise HTTPException(status_code=400, detail="Create watch failed")
    return Message(msg='Success')


def delete_argue_watch(db: Session, argue_id: int, user: UserInDB) -> Message:
    watch = crud_argue.delete_argue_watch(db, argue_id, user)
    if watch is None:
        raise HTTPException(status_code=400, detail="Watch does not exist")
    return Message(msg='Success')


def create_argue_vote(db: Session, vote: ArguePostVoteCreate, user: UserInDB) -> Message:
    # TODO: 检查是否已投过票
    vote = crud_argue.create_argue_vote(db, vote, user)
    if vote is None:
        raise HTTPException(status_code=400, detail="Create vote failed")
    return Message(msg='Success')


def create_argue_attachment(db: Session, attachment: ArguePostAttachmentCreate) -> Message:
    attachment = crud_argue.create_argue_attachment(db, attachment)
    if attachment is None:
        raise HTTPException(status_code=400, detail="Create attachment failed")
    return Message(msg='Success')


def delete_argue_attachment(db: Session, file_id: uuid.UUID) -> Message:
    attachment = crud_argue.delete_argue_attachment(db, file_id)
    if attachment is None:
        raise HTTPException(status_code=400, detail="Attachment does not exist")
    return Message(msg='Success')


def create_argue_feedback(db: Session, feedback: ArguePostFeedbackCreate, user: UserInDB) -> ArguePostFeedback:
    feedback_entity = crud_argue.create_feedback(db, feedback, user)
    if feedback_entity is None:
        raise HTTPException(status_code=400, detail="Create feedback failed")
    return argue2feedback(feedback_entity.argue_post)


def create_argue_feedback_attachment(db: Session, attachment: ArguePostFeedbackAttachmentCreate) -> Message:
    attachment = crud_argue.create_feedback_attachment(db, attachment)
    if attachment is None:
        raise HTTPException(status_code=400, detail="Attachment does not exist")
    return Message(msg='Success')


def delete_argue_feedback_attachment(db: Session, file_id) -> Message:
    attachment = crud_argue.delete_feedback_attachment(db, file_id)
    if attachment is None:
        raise HTTPException(status_code=400, detail="Attachment does not exist")
    return Message(msg='Success')