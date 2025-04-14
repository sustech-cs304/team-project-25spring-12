import uuid

from fastapi import APIRouter, UploadFile, Depends, Form, File

from mjc.model.schema.common import File as FileSchema
from mjc.model.schema.user import UserInDB
from mjc.service.user import get_current_user
from mjc.utils.database import SessionDep
from mjc.service import common as common_service
from mjc.model.entity import Visibility


router = APIRouter()


@router.get("/file/{file_id}", response_model=FileSchema)
async def get_file(db: SessionDep, file_id: uuid.UUID):
    return common_service.get_local_resource_file(db=db, file_id=file_id)


@router.post("/file", response_model=FileSchema)
async def create_file(db: SessionDep, file: UploadFile = File(),
                      visibility: str = Form(),
                      current_user: UserInDB = Depends(get_current_user)):
    return await common_service.create_local_resource_file(db=db, file=file, visibility=Visibility(visibility), uploader=current_user)