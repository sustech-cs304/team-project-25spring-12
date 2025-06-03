import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from mjc.model.schema.common import Message
from mjc.model.schema.widget import DocWidget, DocWidgetCreate, DocWidgetUpdate, \
    AssignmentWidget, AssignmentWidgetCreate, AssignmentWidgetUpdate, \
    WidgetAttachmentCreate, \
    NotePdfWidget, NotePdfWidgetCreate, NotePdfWidgetUpdate, Note, NoteCreate, NoteUpdate
from mjc.model.schema.user import UserInDB
from mjc.service import user as user_service
from mjc.service import widget as widget_service
from mjc.utils.database import SessionDep
from mjc.permission import widget as widget_permission


router = APIRouter()


@router.post(path="/class/widget/doc", response_model=DocWidget,
             dependencies=[Depends(widget_permission.verify_widget_create)])
async def create_doc_widget(db: SessionDep,
                            widget: DocWidgetCreate,
                            current_user: UserInDB = Depends(user_service.get_current_user)):
    return widget_service.create_doc_widget(db, current_user, widget)


@router.patch(path="/class/widget/doc", response_model=DocWidget,
              dependencies=[Depends(widget_permission.verify_widget_update)])
async def update_doc_widget(db: SessionDep,
                            widget: DocWidgetUpdate,
                            current_user: UserInDB = Depends(user_service.get_current_user)):
    return widget_service.update_doc_widget(db, current_user, widget)


@router.post(path="/class/widget/assignment", response_model=AssignmentWidget,
             dependencies=[Depends(widget_permission.verify_widget_create)])
async def create_assignment_widget(db: SessionDep,
                                   widget: AssignmentWidgetCreate,
                                   current_user: UserInDB = Depends(user_service.get_current_user)):
    return widget_service.create_assignment_widget(db, current_user, widget)


@router.patch(path="/class/widget/assignment", response_model=AssignmentWidget,
              dependencies=[Depends(widget_permission.verify_widget_update)])
async def update_assignment_widget(db: SessionDep,
                                   widget: AssignmentWidgetUpdate,
                                   current_user: UserInDB = Depends(user_service.get_current_user)):
    return widget_service.update_assignment_widget(db, current_user, widget)


@router.post(path="/class/widget/notepdf", response_model=NotePdfWidget,
             dependencies=[Depends(widget_permission.verify_widget_create)])
async def create_note_pdf_widget(db: SessionDep,
                                 widget: NotePdfWidgetCreate,
                                 current_user: UserInDB = Depends(user_service.get_current_user)):
    return widget_service.create_note_pdf_widget(db, current_user, widget)


@router.patch(path="/class/widget/notepdf", response_model=NotePdfWidget,
              dependencies=[Depends(widget_permission.verify_widget_update)])
async def update_note_pdf_widget(db: SessionDep,
                                 widget: NotePdfWidgetUpdate,
                                 current_user: UserInDB = Depends(user_service.get_current_user)):
    return widget_service.update_note_pdf_widget(db, current_user, widget)


@router.post(path="/class/widget/attachment", response_model=Message,
             dependencies=[Depends(widget_permission.verify_add_attach)])
async def add_widget_attachment(db: SessionDep, attach: WidgetAttachmentCreate):
    return widget_service.add_widget_attachment(db, attach)


@router.delete(path="/class/widget/attachment/{file_id}", response_model=Message,
               dependencies=[Depends(widget_permission.verify_delete_attach)])
async def delete_widget_attachment(db: SessionDep, file_id: uuid.UUID):
    return widget_service.delete_attachment(db, file_id)


@router.post(path="/class/widget/notepdf/note", response_model=Note,
             dependencies=[Depends(widget_permission.verify_add_note)])
async def create_note(db: SessionDep, note: NoteCreate,
                      current_user: UserInDB = Depends(user_service.get_current_user)):
    return widget_service.create_note(db, note, current_user)


@router.patch(path="/class/widget/notepdf/note", response_model=Note,
              dependencies=[Depends(widget_permission.verify_update_note)])
async def update_note(db: SessionDep, note: NoteUpdate,
                      current_user: UserInDB = Depends(user_service.get_current_user)):
    return widget_service.update_note(db, note, current_user)


@router.delete(path="/class/widget/{widget_id}", status_code=status.HTTP_200_OK,
               dependencies=[Depends(widget_permission.verify_widget_delete)])
async def delete_widget(db: SessionDep, widget_id: int):
    return widget_service.delete_widget(db, widget_id)


@router.delete(path="/class/widget/notepdf/note/{note_id}", status_code=status.HTTP_200_OK,
               dependencies=[Depends(widget_permission.verify_delete_note)])
async def delete_note(db: SessionDep, note_id: int, current_user: UserInDB = Depends(user_service.get_current_user)):
    return widget_service.delete_note(db, note_id, current_user)


@router.get(path="/class/widget/{widget_id}", response_model=AssignmentWidget | NotePdfWidget | DocWidget)
async def get_widget(db: SessionDep, widget_id: int, current_user: UserInDB = Depends(user_service.get_current_user)):
    return widget_service.get_widget(db, widget_id, current_user)
