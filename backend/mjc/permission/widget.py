import uuid

from fastapi import Depends, HTTPException, status
from sqlmodel import Session

from mjc.utils.database import SessionDep
from mjc.model.schema.user import UserInDB
from mjc.model.schema.widget import WidgetCreate, WidgetUpdate, WidgetAttachmentCreate, NoteCreate, NoteUpdate
from mjc.service.user import get_current_user
from mjc.crud import page as crud_page, widget as crud_widget, common as crud_common
from mjc.permission.common import verify_class_admin, verify_user_in_class


def verify_widget_exist(db: Session, widget_id: int):
    widget = crud_widget.get_widget(db, widget_id)
    if widget is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Widget not found")
    return widget


async def verify_widget_create(db: SessionDep, widget: WidgetCreate,
                               current_user: UserInDB = Depends(get_current_user)):
    page = crud_page.get_page(db, widget.page_id)
    if page is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Page not found")
    verify_class_admin(db, page.class_id, current_user)


async def verify_widget_update(db: SessionDep, widget: WidgetUpdate,
                                current_user: UserInDB = Depends(get_current_user)):
    widget = verify_widget_exist(db, widget.id)
    verify_class_admin(db, widget.page.class_id, current_user)


async def verify_widget_delete(db: SessionDep, widget_id: int,
                               current_user: UserInDB = Depends(get_current_user)):
    widget = crud_widget.get_widget(db, widget_id)
    verify_class_admin(db, widget.page.class_id, current_user)


async def verify_add_attach(db: SessionDep, attach: WidgetAttachmentCreate,
                            current_user: UserInDB = Depends(get_current_user)):
    verify_widget_exist(db, attach.widget_id)
    widget = crud_widget.get_widget(db, attach.widget_id)
    verify_user_in_class(db, widget.page.class_id, current_user)


async def verify_delete_attach(db: SessionDep, file_id: uuid.UUID):
    if crud_common.get_local_resource_file(db, file_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")


async def verify_add_note(db: SessionDep, note: NoteCreate,
                          current_user: UserInDB = Depends(get_current_user)):
    widget = crud_widget.get_widget(db, note.widget_id)
    verify_user_in_class(db, widget.page.class_id, current_user)


async def verify_update_note(db: SessionDep, note: NoteUpdate,
                             current_user: UserInDB = Depends(get_current_user)):
    note = crud_widget.get_note(db, note.note_id)
    verify_user_in_class(db, note.class_id, current_user)


async def verify_delete_note(db: SessionDep, note_id: int,
                             current_user: UserInDB = Depends(get_current_user)):
    note = crud_widget.get_note(db, note_id)
    verify_user_in_class(db, note.note_pdf_widget.widget.page.class_id, current_user)
