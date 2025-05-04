from app.models.base import BaseMongoDBModel
from app.core.security import create_api_key
from datetime import datetime
from pydantic import Field
from app.common.constants.account_type_enum import AccountType

class Account(BaseMongoDBModel): 
    username: str
    fullname: str = ""
    email: str = ""
    avatar_url: str = ""
    hashed_password: str
    account_type: AccountType = AccountType.USER
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
    api_key: str = Field(default_factory=create_api_key)


# TODO: add methods to create SYSTEM, ADMIN accounts