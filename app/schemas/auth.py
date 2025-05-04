from pydantic import BaseModel


class AuthBase(BaseModel): 
    password: str
    fullname: str = ""
    email: str = ""
    avatar_url: str = ""  # TODO: create avatar upload endpoint

class AuthCreate(AuthBase): 
    username: str
    email: str = ""


class AuthUpdate(AuthBase): 
    pass


class AuthParams(BaseModel): 
    searchable_fields: list[str] = ["fullname", "email"]