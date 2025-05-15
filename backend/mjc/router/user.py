from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

import mjc.model.schema.user
from mjc.model.schema.user import UserInDB
from mjc.service import user as user_service
from mjc.utils.database import SessionDep

router = APIRouter()


@router.post("/user/login", response_model=mjc.model.schema.user.Token)
async def login(db: SessionDep, form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return user_service.login(db, form.username, form.password)


@router.post("/user/register", response_model=mjc.model.schema.user.Profile)
async def register(db: SessionDep, user: mjc.model.schema.user.UserCreate):
    return user_service.register(db, user)


@router.get("/user/me", response_model=mjc.model.schema.user.Profile)
async def get_profile_me(db: SessionDep,
                         current_user: UserInDB = Depends(user_service.get_current_user)):
    return user_service.get_profile(db, current_user.username)


@router.get("/user/{username}", response_model=mjc.model.schema.user.Profile)
async def get_profile(db: SessionDep, username: str):
    return user_service.get_profile(db, username)