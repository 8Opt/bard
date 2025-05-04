from app.db.mongo.base import BaseMongoDBRepository
from app.models.auth import Account
from app.schemas.auth import AuthParams, AuthCreate, AuthUpdate
from app.core.security import verify_password
from typing import Optional 

class AuthRepository(BaseMongoDBRepository[Account, AuthCreate, AuthUpdate]):
    def __init__(self):
        super().__init__(Account)
        self.searchable_fields = AuthParams.searchable_fields



    @classmethod
    async def get_by_username(cls, *, username: str) -> Optional["Account"]:
        # Because all usernames are converted to lowercase at user creation,
        # make the given 'username' parameter also lowercase.
        return await cls.find_one(cls.username == username.lower())

    @classmethod
    async def get_by_api_key(cls, *, api_key: str) -> Optional["Account"]:
        return await cls.find_one(cls.api_key == api_key.lower())

    @classmethod
    async def authenticate(
        cls,
        *,
        username: str,
        password: str,
    ) -> Optional["Account"]:
        account: Account = await cls.get_by_username(username=username)
        if not account or not verify_password(password, account.hashed_password):
            return None
        return account