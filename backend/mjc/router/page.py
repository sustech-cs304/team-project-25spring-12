from email.policy import default
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from backend.mjc.model.schema.page import Page, PageCreate, PageUpdate

from backend.mjc.service import page as page_service
from backend.mjc.utils.database import SessionDep

router = APIRouter()


@router.post(path="/class/page", response_model=Page)
async def create_page(db:SessionDep, page: PageCreate):
    return page_service.create_page(db, page)


@router.patch(path="/class/page", response_model=Page)
async def update_page(db:SessionDep, page: PageUpdate):
    return page_service.update_page(db, page)


@router.delete(path="/class/page/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_page(db:SessionDep, id:int):
    return page_service.delete_page(db, id)
