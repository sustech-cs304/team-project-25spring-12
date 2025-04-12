from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from backend.mjc.model.schema.widget import DocWidget, DocWidgetCreate, DocWidgetUpdate, \
    AssignmentWidget, AssignmentWidgetCreate, AssignmentWidgetUpdate, \
    NotePdfWidget, NotePdfWidgetCreate, NotePdfWidgetUpdate, Note, NoteCreate, NoteUpdate
from backend.mjc.model.schema.user import UserInDB
from backend.mjc.service import user as user_service
from backend.mjc.service import widget as widget_service
from backend.mjc.utils.database import SessionDep


router = APIRouter()


@router.post(path="/class/widget/doc", response_model=DocWidget)
async def create_doc_widget(db: SessionDep,
                            widget: DocWidgetCreate,
                            current_user: UserInDB = Depends(user_service.get_current_user)):
    return widget_service.create_doc_widget(db, current_user, widget)


@router.patch(path="/class/widget/doc", response_model=DocWidget)
async def update_doc_widget(db: SessionDep,
                            widget: DocWidgetUpdate,
                            current_user: UserInDB = Depends(user_service.get_current_user)):
    return widget_service.update_doc_widget(db, current_user, widget)


@router.post(path="/class/widget/assignment", response_model=AssignmentWidget)
async def create_assignment_widget(db: SessionDep,
                                   widget: AssignmentWidgetCreate,
                                   current_user: UserInDB = Depends(user_service.get_current_user)):
    return widget_service.create_assignment_widget(db, current_user, widget)


@router.patch(path="/class/widget/assignment", response_model=AssignmentWidget)
async def update_assignment_widget(db: SessionDep,
                                   widget: AssignmentWidgetUpdate,
                                   current_user: UserInDB = Depends(user_service.get_current_user)):
    return widget_service.update_assignment_widget(db, current_user, widget)


@router.post(path="/class/widget/notepdf", response_model=NotePdfWidget)
async def create_note_pdf_widget(db: SessionDep,
                                 widget: NotePdfWidgetCreate,
                                 current_user: UserInDB = Depends(user_service.get_current_user)):
    return widget_service.create_note_pdf_widget(db, current_user, widget)


@router.patch(path="/class/widget/notepdf", response_model=NotePdfWidget)
async def update_note_pdf_widget(db: SessionDep,
                                 widget: NotePdfWidgetUpdate,
                                 current_user: UserInDB = Depends(user_service.get_current_user)):
    return widget_service.update_note_pdf_widget(db, current_user, widget)


@router.post(path="/class/widget/notepdf/note", response_model=Note)
async def create_note(db: SessionDep, note: NoteCreate,
                      current_user: UserInDB = Depends(user_service.get_current_user)):
    return widget_service.create_note(db, note, current_user)


@router.patch(path="/class/widget/notepdf/note", response_model=Note)
async def update_note(db: SessionDep, note: NoteUpdate,
                      current_user: UserInDB = Depends(user_service.get_current_user)):
    return widget_service.update_note(db, note, current_user)


@router.delete(path="/class/widget/{widget_id}", status_code=status.HTTP_200_OK)
async def delete_widget(db: SessionDep, widget_id: int):
    return widget_service.delete_widget(db, widget_id)


@router.delete(path="/class/widget/notepdf/note/note_id}", status_code=status.HTTP_200_OK)
async def delete_note(db: SessionDep, note_id: int):
    return widget_service.delete_note(db, note_id)