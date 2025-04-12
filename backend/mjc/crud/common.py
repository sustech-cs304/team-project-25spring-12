import uuid
from datetime import datetime

from sqlmodel import Session, select

from backend.mjc.model.schema.common import LocalResourceFileCreate
from backend.mjc.model.schema.user import UserInDB
from backend.mjc.model.entity import LocalResourceFile


def create_local_resource_file(db: Session, file: LocalResourceFileCreate, uploader: UserInDB) -> LocalResourceFile:
    file_entity = LocalResourceFile(
        id=file.id,
        upload_time=datetime.now(),
        uploader_username=uploader.username,
        filename=file.filename,
        system_path=file.system_path,
        visibility=file.visibility
    )
    db.add(file_entity)
    db.commit()
    db.refresh(file_entity)
    return file_entity


def get_local_resource_file(db: Session, file_id: uuid.UUID) -> LocalResourceFile:
    stmt = select(LocalResourceFile).where(LocalResourceFile.id == file_id) \
                                    .where(LocalResourceFile.is_deleted == False)
    file_entity = db.exec(stmt).first()
    return file_entity