
from datetime import datetime
from typing import List

from pydantic import BaseModel, PositiveInt, field_validator, EmailStr, UUID4



class UserBase(BaseModel):
    email: EmailStr



class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: UUID4
    roles: list | None = None

    class Config:
        orm_mode = True
        from_attributes = True





class UserRegister(UserBase):
    password: str
    confirmPassword: str
    class Config:
        orm_mode = True
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True
        from_attributes = True


class JwtTokenSchema(BaseModel):
    token: str
    payload: dict
    expire: datetime

    class Config:
        orm_mode = True
        from_attributes = True



class TokenPair(BaseModel):
    access: JwtTokenSchema
    refresh: JwtTokenSchema

    class Config:
        orm_mode = True
        from_attributes = True




class RefreshToken(BaseModel):
    refresh: str

    class Config:
        orm_mode = True
        from_attributes = True

class AccessToken(BaseModel):
    access: str

    class Config:
        orm_mode = True
        from_attributes = True
class SuccessResponseScheme(BaseModel):
    msg: str

    class Config:
        orm_mode = True
        from_attributes = True


class BlackListToken(BaseModel):
    id: UUID4
    expire: datetime



# changes --------------------------

class Permission(BaseModel):
    name: str
    description: str


class Role(BaseModel):
    name: str

class Group(BaseModel):
    name: str


