import datetime

from pydantic import BaseModel


class UserUpdate(BaseModel):
    username: str
    email: str
    entreprise: str
    admin: bool = False

    class Config:
        from_attributes = True


class User(BaseModel):
    id: int
    username: str
    email: str
    entreprise: str
    admin: bool

    class Config:
        from_attributes = True
