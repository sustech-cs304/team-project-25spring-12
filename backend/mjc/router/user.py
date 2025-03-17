from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ..model import schemas
from ..model.schemas import UserInDB
from ..service import user as user_service
from ..crud import user as user_crud
from ..utils.database import SessionDep
from ..utils import security

router = APIRouter()


@router.post("/user/login", response_model=schemas.Token)
async def login(db: SessionDep, form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return user_service.login(db, form.username, form.password)


@router.post("/user/register", response_model=schemas.Profile)
async def register(db: SessionDep, user: schemas.UserCreate):
    return user_service.register(db, user)


@router.get("/user/{username}", response_model=schemas.Profile)
async def get_profile(db: SessionDep, username: str):
    return user_service.get_profile(db, username)


@router.get("/user/me", response_model=schemas.Profile)
async def get_profile_me(db: SessionDep,
                         current_user: schemas.UserInDB = Annotated[UserInDB, Depends(user_service.get_current_user)]):
    return user_service.get_profile(db, current_user.username)