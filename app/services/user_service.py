from app.models.user import User
from app.database.postgres import async_session
from sqlalchemy.future import select
from app.core.security import get_password_hash, verify_password

class UserService:
    @staticmethod
    async def create_user(user_data):
        async with async_session() as session:
            user = User(
                username=user_data.username,
                hashed_password=get_password_hash(user_data.password)
            )
            session.add(user)
            await session.commit()
            return user

    @staticmethod
    async def authenticate_user(username: str, password: str):
        async with async_session() as session:
            result = await session.execute(select(User).filter_by(username=username))
            user = result.scalars().first()
            if user and verify_password(password, user.hashed_password):
                return user
            return None