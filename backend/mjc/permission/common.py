from fastapi import HTTPException, status, Depends

from mjc.model.schema.user import UserInDB
from mjc.service.user import get_current_user


async def verify_admin(current_user: UserInDB = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not system admin")