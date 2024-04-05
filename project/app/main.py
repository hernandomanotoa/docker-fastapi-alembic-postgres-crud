from fastapi import Depends, FastAPI, Body, HTTPException, Path, Query, Request
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer
from faker import Faker

from app.db import get_session, init_db
from app.models import Song, SongCreate, User, UserCreate
from app.jwt_manager import create_token, validate_token

app = FastAPI()
app.title = "Mi aplicación con  FastAPI"
app.version = "0.0.1"

fake = Faker()
# descomentar para crear la base de datos
# @app.on_event("startup")
# async def on_startup():
#     init_db()

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@admin.com":
            raise HTTPException(status_code=403, detail="Credenciales son invalidas")


@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Bienvenido a fastapi</h1>')

@app.post('/login', tags=['auth'])
def login(user: UserCreate):
    if user.email == "admin@admin.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)

@app.get("/songs_add", tags=['songs'])
async def add_songs(session: AsyncSession = Depends(get_session)):
    for _ in range(10):  # Generar 10 registros de ejemplo
        new_song = Song(name=fake.catch_phrase(), artist=fake.name(), year=fake.random_int(min=2000, max=2024))
        session.add(new_song)
    session.commit()
    return JSONResponse(status_code=201, content={"message": "Se ha agregado 10 canciones"})

@app.get("/songs", tags=['songs'], response_model=list[Song], status_code=200)
async def get_songs(session: AsyncSession = Depends(get_session)):
    result = session.execute(select(Song))
    songs = result.scalars().all()
    songs_data = [{"name": song.name, "artist": song.artist, "year": song.year, "id": song.id} for song in songs]
    return JSONResponse(status_code=200, content=songs_data)
    # return [Song(name=song.name, artist=song.artist, year=song.year, id=song.id) for song in songs]
    

@app.get("/songs/{id}", tags=['songs'], response_model=Song)
async def get_song(id: int, session: AsyncSession = Depends(get_session)):
    song=session.query(Song).filter(Song.id==id).first()
    if song is None:
        return JSONResponse(status_code=404, content={"message": "Song not found"})
    
    song_data = {
        "name": song.name,
        "artist": song.artist,
        "year": song.year,
        "id": song.id
    }
    return JSONResponse(content=song_data)

@app.post("/songs", tags=['songs'])
async def add_song(song: SongCreate, session: AsyncSession = Depends(get_session)):
    song = Song(name=song.name, artist=song.artist, year=song.year)
    session.add(song)
    session.commit()
    session.refresh(song)
    return JSONResponse(status_code=201, content={"message": "Se ha registrado la canción"})


@app.put("/songs/{id}", tags=['songs'])
async def update_song(id: int, song: SongCreate, session: AsyncSession = Depends(get_session), status_code=200):
    song_old=session.query(Song).filter(Song.id==id).first()
    if song_old is None:
        return JSONResponse(status_code=404, content={"message": "Canción no encontrada no se puede actualizar"})
    song_old.name = song.name
    song_old.artist = song.artist
    song_old.year = song.year
    session.add(song_old)
    session.commit()
    return JSONResponse(status_code=200, content={"message": "Se ha modificado la canción"})


    
@app.delete("/songs/{id}", tags=['songs'], status_code=200)
async def delete_song(id: int, session: AsyncSession = Depends(get_session)):
    song=session.query(Song).filter(Song.id==id).first()
    if song is None:
        return JSONResponse(status_code=404, content={"message": "Canción no encontrada, no se puede eliminar"})
    session.delete(song)
    session.commit()
    return JSONResponse(status_code=200, content={"message": "Se ha eliminado la canción"})
