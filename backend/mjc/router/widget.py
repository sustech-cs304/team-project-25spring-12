from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from backend.mjc.model.schema.widget import DocWidget, DocWidgetCreate
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