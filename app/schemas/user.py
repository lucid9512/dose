from fastapi_users import schemas

class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    is_active: bool
    is_superuser: bool

class UserCreate(schemas.BaseUserCreate):
    email: str
    password: str

class UserUpdate(schemas.BaseUserUpdate):
    password: str | None = None
    is_active: bool | None = None
    is_superuser: bool | None = None