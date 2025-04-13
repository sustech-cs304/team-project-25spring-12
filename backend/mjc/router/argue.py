import uuid
from fastapi import APIRouter, Depends

from backend.mjc.utils.database import SessionDep
from backend.mjc.service.user import get_current_user
from backend.mjc.service import argue as argue_service
from backend.mjc.model.schema.argue import ArguePost, ArguePostCard, ArguePostCreate, ArguePostUpdate, ArguePostComment, \
    ArguePostCommentCreate, ArguePostWatchCreate, ArguePostVoteCreate, ArguePostAttachmentCreate, ArguePostFeedback, \
    ArguePostFeedbackCreate, ArguePostFeedbackAttachmentCreate
from backend.mjc.model.schema.common import Message

router = APIRouter()


@router.get('/argue', response_model=list[ArguePostCard])
async def get_argues(db: SessionDep, current_user = Depends(get_current_user)):
    return argue_service.get_argues(db, current_user)


@router.post('/argue', response_model=ArguePost)
async def create_argue(db: SessionDep, argue: ArguePostCreate,
                       current_user = Depends(get_current_user)):
    return argue_service.create_argue(db, argue, current_user)


@router.get('/argue/{argue_id}', response_model=ArguePost)
async def get_argue(db: SessionDep, argue_id: int):
    return argue_service.get_argue(db, argue_id)


@router.patch('/argue/{argue_id}', response_model=ArguePost)
async def update_argue(db: SessionDep, argue: ArguePostUpdate):
    return argue_service.update_argue(db, argue)


@router.delete('/argue/{argue_id}', response_model=Message)
async def delete_argue(db: SessionDep, argue_id: int):
    return argue_service.delete_argue(db, argue_id)


@router.post('/argue/comment', response_model=ArguePostComment)
async def create_argue_comment(db: SessionDep, comment: ArguePostCommentCreate,
                               current_user = Depends(get_current_user)):
    return argue_service.create_argue_comment(db, comment, current_user)


@router.post('/argue/watch', response_model=Message)
async def create_argue_watch(db: SessionDep, comment: ArguePostWatchCreate,
                             current_user = Depends(get_current_user)):
    return argue_service.create_argue_watch(db, comment, current_user)


@router.post('/argue/{argue_id}/watch', response_model=Message)
async def delete_argue_watch(db: SessionDep, argue_id: int,
                             current_user = Depends(get_current_user)):
    return argue_service.delete_argue_watch(db, argue_id, current_user)


@router.post('/argue/vote', response_model=Message)
async def create_argue_vote(db: SessionDep, vote: ArguePostVoteCreate,
                            current_user = Depends(get_current_user)):
    return argue_service.create_argue_vote(db, vote, current_user)


@router.post('/argue/attachment', response_model=Message)
async def create_argue_attachment(db: SessionDep, attachment: ArguePostAttachmentCreate):
    return argue_service.create_argue_attachment(db, attachment)


@router.delete('/argue/attachment/{file_id}', response_model=Message)
async def delete_argue_attachment(db: SessionDep, file_id: uuid.UUID):
    return argue_service.delete_argue_attachment(db, file_id)


@router.post('/argue/feedback', response_model=ArguePostFeedback)
async def create_argue_feedback(db: SessionDep, feedback: ArguePostFeedbackCreate,
                                current_user = Depends(get_current_user)):
    return argue_service.create_argue_feedback(db, feedback, current_user)


@router.post('/argue/feedback/attachment', response_model=Message)
async def create_argue_feedback_attachment(db: SessionDep, attachment: ArguePostFeedbackAttachmentCreate):
    return argue_service.create_argue_feedback_attachment(db, attachment)


@router.delete('/argue/feedback/attachment/{file_id}', response_model=Message)
async def delete_argue_feedback_attachment(db: SessionDep, file_id: uuid.UUID):
    return argue_service.delete_argue_feedback_attachment(db, file_id)