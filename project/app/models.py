from sqlmodel import SQLModel, Field
from typing import Optional
from faker import Faker
fake = Faker()

class SongBase(SQLModel):
    name: str = Field(default=fake.catch_phrase())
    artist: str = Field(default=fake.name())
    year: Optional[int] = Field(default=fake.random_int(min=2000, max=2024))

class Song(SongBase, table=True):
    id: int = Field(default=None, primary_key=True)
    # id: int = Field(default=None, nullable=False, primary_key=True)

class SongCreate(SongBase):
    pass

class UserBase(SQLModel):
    email:str = Field(default="admin@admin.com")
    password:str = Field(default="admin")
    # email:str
    # password:str
    
class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    
class UserCreate(UserBase):
    pass


class MovieBase(SQLModel):
    title: str = Field(default=fake.catch_phrase())
    overview: str = Field(default=fake.catch_phrase())
    year: int = Field(default=fake.random_int(min=2000, max=2024))
    rating: float = Field(default=fake.random_int(min=1, max=10))
    category: str = Field(default=fake.country())
        
class Movie(MovieBase, table=True):
    id: int = Field(default=None, primary_key=True)
    
class MovieCreate(MovieBase):
    pass
    
