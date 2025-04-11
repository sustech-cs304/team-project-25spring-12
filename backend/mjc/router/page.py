from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from backend.mjc.model.schema.page import Page, PageCreate

from backend.mjc.service import page as page_service
from backend.mjc.utils.database import SessionDep

router = APIRouter()


@router.post(path="/class/page", response_model=Page)
async def create_page(db:SessionDep,
                      page: PageCreate,
                      ):
    return page_service.create_page(db, page)