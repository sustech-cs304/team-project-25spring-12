import uuid
from os import path
import aiofiles
from aip import AipOcr

from fastapi import UploadFile
from fastapi.responses import FileResponse
from sqlmodel import Session

from mjc.model.entity.common import Visibility
from mjc.model.schema.user import UserInDB
from mjc.model.schema.common import LocalResourceFileCreate, File
from mjc.crud import common as common_crud
from mjc import config


async def create_local_resource_file(db: Session, file: UploadFile, visibility: Visibility, uploader: UserInDB) -> File:
    file_id = uuid.uuid4()
    filename = f'{file_id}_{file.filename}'
    system_path = path.join(config.FILE_SAVE_ADDRESS, filename)
    async with aiofiles.open(system_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)

    file_create = LocalResourceFileCreate(
        id=file_id,
        filename=file.filename,
        system_path=system_path,
        visibility=visibility
    )
    file_entity = common_crud.create_local_resource_file(db, file_create, uploader)
    return File.model_validate(file_entity.model_dump())


def get_local_resource_file(db: Session, file_id: uuid.UUID) -> FileResponse:
    file = common_crud.get_local_resource_file(db, file_id)
    return FileResponse(file.system_path)


def ocr4pdf(db: Session, file_id: uuid.UUID) -> str:
    file = common_crud.get_local_resource_file(db, file_id)
    with open(file.system_path, 'rb') as pf:
        pdf_file = pf.read()

    result = ''
    client = AipOcr(config.OCR_APP_ID, config.OCR_API_KEY, config.OCR_SECRET_KEY)

    # 第一页
    res_pdf = client.basicGeneralPdf(pdf_file)
    for word in res_pdf['words_result']:
        result += word['words']
    # 剩余页
    if int(res_pdf['pdf_file_size']) > 1:
        for page_num in range(2, int(res_pdf['pdf_file_size']) + 1):
            res_pdf = client.basicGeneralPdf(pdf_file, {"pdf_file_num": page_num})
            for word in res_pdf['words_result']:
                result += word['words']
    return result
