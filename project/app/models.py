from sqlmodel import SQLModel, Field
from typing import Optional


class SongBase(SQLModel):
    name: str
    artist: str
    year: Optional[int] = None

class Song(SongBase, table=True):
    id: int = Field(default=None, primary_key=True)
    # id: int = Field(default=None, nullable=False, primary_key=True)

class SongCreate(SongBase):
    pass

class UserBase(SQLModel):
    email:str = Field(default="admin@admin.com")
    password:str = Field(default="admin2")
    # email:str
    # password:str
    
class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    
class UserCreate(UserBase):
    pass


class Movie(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    overview: str
    year: int
    rating: float
    category: str