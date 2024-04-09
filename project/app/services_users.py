from sqlmodel import select
from app.models import User, UserCreate

class UserService():
    
    def __init__(self, db) -> None:
        self.db = db

    async def get_users(self):
        result = await self.db.execute(select(User))
        result = result.scalars().all()
        return result

    async def get_user(self, id):
        users = await self.db.execute(select(User).where(User.id==id))
        result = users.scalars().first()
        return result

    async def get_users_by_email_password(self, data: UserCreate):
        users = await self.db.execute(select(User).where(User.email==data.email and User.password==data.password))
        result = users.scalars().first()
        return result

    async def create_user(self, user: User):
        # user = User(title=user.title, overview=user.overview, year=user.year, rating=user.rating, category=user.category)
        new_user = User(**user.dict())
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return

    async def update_user(self, id: int, data: UserCreate):
        user_old = await UserService(self.db).get_user(id)
        user_old.email = data.email
        user_old.password = data.password
        self.db.add(user_old)
        await self.db.commit()
        return

    async def delete_user(self, id: int):
        user = await UserService(self.db).get_user(id)
        await self.db.delete(user)
        await self.db.commit()
        return