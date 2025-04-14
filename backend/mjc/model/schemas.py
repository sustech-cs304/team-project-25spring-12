from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    is_active: bool = True
    is_admin: bool = False


class UserInDB(UserBase):
    """
    用于用户信息缓存
    """
    username: str
    encoded_password: str


class UserCreate(UserBase):
    password: str
    name: str
    department: str | None
    email: str | None


class Profile(UserBase):
    name: str
    department: str | None
    email: str | None


class ChangePassword(BaseModel):
    old_password: str
    new_password: str


class Token(BaseModel):
    access_token: str
