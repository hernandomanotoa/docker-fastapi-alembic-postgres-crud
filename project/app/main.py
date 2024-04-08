from fastapi import Depends, FastAPI, Body, HTTPException, Path, Query, Request
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer
from faker import Faker

from app.db import get_session, init_db
from app.models import Song, SongCreate, Movie
# from app.jwt_manager import create_token, validate_token

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

# @app.post('/login', tags=['auth'])
# def login(user: UserCreate):
#     if user.email == "admin@admin.com" and user.password == "admin":
#         token: str = create_token(user.dict())
#         return JSONResponse(status_code=200, content=token)

@app.get("/songs_add/{numero}", tags=['songs'])
async def add_songs(numero: int, session: AsyncSession = Depends(get_session)):
    for _ in range(numero):  # Generar 10 registros de ejemplo
        new_song = Song(name=fake.catch_phrase(), artist=fake.name(), year=fake.random_int(min=2000, max=2024))
        session.add(new_song)
    await session.commit()
    return JSONResponse(status_code=201, content={"message": "Se ha agregado canciones: " + str(numero)})

@app.get("/songs", tags=['songs'], response_model=list[Song])
async def get_songs(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Song))
    songs = result.scalars().all()
    songs_data = [{"name": song.name, "artist": song.artist, "year": song.year, "id": song.id} for song in songs]
    return JSONResponse(status_code=200, content=songs_data)


@app.get("/songs/{id}", tags=['songs'], response_model=list[Song])
async def get_song(id: int, session: AsyncSession = Depends(get_session)):
    songs = await session.execute(select(Song).where(Song.id==id))
    songs = songs.scalars().first()
    songs_data = [{"name": song.name, "artist": song.artist, "year": song.year, "id": song.id} for song in songs]
    return JSONResponse(status_code=200, content=songs_data)

@app.post("/songs", tags=['songs'])
async def add_song(song: SongCreate, session: AsyncSession = Depends(get_session)):
    song = Song(name=song.name, artist=song.artist, year=song.year)
    session.add(song)
    await session.commit()
    await session.refresh(song)
    return JSONResponse(status_code=201, content={"message": "Se ha registrado la canción"})

@app.put("/songs/{id}", tags=['songs'])
async def update_song(id: int, song: SongCreate, session: AsyncSession = Depends(get_session)):
    song_old = await session.execute(select(Song).where(Song.id==id))
    song_old = song_old.scalars().first()
    if song_old == None:
        return JSONResponse(status_code=404, content={"message": "Canción no encontrada no se puede actualizar"})
    song_old.name = song.name
    song_old.artist = song.artist
    song_old.year = song.year
    session.add(song_old)
    await session.commit()
    return JSONResponse(status_code=200, content={"message": "Se ha modificado la canción"})

@app.delete("/songs/{id}", tags=['songs'], status_code=201)
async def delete_song(id: int, session: AsyncSession = Depends(get_session)):
    songs = await session.execute(select(Song).where(Song.id==id))
    songs = songs.scalars().first()
    if songs == None:
        return JSONResponse(status_code=201, content={"mensaje":"No se encuentra el item a eliminar"})
    else:
    # songs = result.scalars().one()
        
        await session.delete(songs)
        await session.commit()
        return JSONResponse(status_code=201, content={"message": "Se ha eliminado la canción"})
    
@app.get("/movies_add/{numero}", tags=['songs'])
async def add_songs(numero: int, session: AsyncSession = Depends(get_session)):
    for _ in range(numero):  # Generar 10 registros de ejemplo
        new_song = Movie(title=fake.catch_phrase(), overview=fake.catch_phrase(), year=fake.random_int(min=2000, max=2024), rating=fake.random_int(min=1, max=10), category=fake.country())
        session.add(new_song)
    await session.commit()
    return JSONResponse(status_code=201, content={"message": "Se ha agregado categorias: " + str(numero)})
