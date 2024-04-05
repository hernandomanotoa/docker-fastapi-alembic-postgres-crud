from fastapi import Depends, FastAPI
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.responses import HTMLResponse, JSONResponse
from app.db import get_session, init_db
from app.models import Song, SongCreate

app = FastAPI()


# @app.on_event("startup")
# async def on_startup():
#     await init_db()


@app.get("/ping")
async def pong():
    return {"ping": "pong!"}


@app.get("/songs", response_model=list[Song])
async def get_songs(session: AsyncSession = Depends(get_session)):
    result = session.execute(select(Song))
    songs = result.scalars().all()
    return [Song(name=song.name, artist=song.artist, year=song.year, id=song.id) for song in songs]


@app.post("/songs")
async def add_song(song: SongCreate, session: AsyncSession = Depends(get_session)):
    song = Song(name=song.name, artist=song.artist, year=song.year)
    session.add(song)
    session.commit()
    session.refresh(song)
    return song

@app.put("/songs/{id}")
async def update_song(id: int, song: SongCreate, session: AsyncSession = Depends(get_session)):
    song_old=session.query(Song).filter(Song.id==id).first()
    song_old.name = song.name
    song_old.artist = song.artist
    song_old.year = song.year
    session.add(song_old)
    session.commit()
    return JSONResponse(content={"message": "Se ha actualizado la canción"})

@app.get("/songs/{id}")
async def get_song(id: int, session: AsyncSession = Depends(get_session)):
    song=session.query(Song).filter(Song.id==id).first()
    return song
    
@app.delete("/songs/{id}")
async def delete_song(id: int, session: AsyncSession = Depends(get_session)):
    song=session.query(Song).filter(Song.id==id).first()
    session.delete(song)
    session.commit()
    return JSONResponse(content={"message": "Se ha eliminado la canción"})