from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = 'mjc_user'  # PostgreSQL 中的 user 表可能会冲突

    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(nullable=False, index=True)
    encoded_password: str = Field(nullable=False)