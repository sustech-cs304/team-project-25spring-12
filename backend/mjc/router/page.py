from email.policy import default
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from mjc.model.schema.common import Message
from mjc.model.schema.page import Page, PageCreate, PageUpdate
from mjc.model.schema.user import UserInDB
from mjc.service import page as page_service
from mjc.service.user import get_current_user
from mjc.utils.database import SessionDep
from mjc.permission import page as page_permission

router = APIRouter()


@router.get(path="/class/page/{page_id}", response_model=Page,
            dependencies=[Depends(page_permission.verify_page_get)])
async def get_page(db:SessionDep, page_id:int, current_user: UserInDB = Depends(get_current_user)):
    return page_service.get_page(db, page_id, current_user)


@router.post(path="/class/page", response_model=Page,
             dependencies=[Depends(page_permission.verify_page_create)])
async def create_page(db:SessionDep, page: PageCreate):
    return page_service.create_page(db, page)


@router.patch(path="/class/page", response_model=Page,
              dependencies=[Depends(page_permission.verify_page_update)])
async def update_page(db:SessionDep, page: PageUpdate):
    return page_service.update_page(db, page)


@router.delete(path="/class/page/{page_id}", response_model=Message,
               dependencies=[Depends(page_permission.verify_page_delete)])
async def delete_page(db:SessionDep, page_id: int):
    return page_service.delete_page(db, page_id)
