from fastapi import Depends, FastAPI, Body, HTTPException, Path, Query, Request
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer
from fastapi.encoders import jsonable_encoder
from faker import Faker

from app.db import get_session, init_db
from app.models import Song, SongCreate, Movie, MovieCreate, UserCreate
from app.error_handler import ErrorHandler
from app.jwt_bearer import create_token, validate_token

app = FastAPI()
app.title = "Mi aplicación con  FastAPI"
app.version = "0.0.1"
app.add_middleware(ErrorHandler)

fake = Faker()
# descomentar para crear la base de datos
# @app.on_event("startup")
# async def on_startup():
#     init_db()

@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Bienvenido a fastapi</h1>')

@app.post('/login', tags=['auth'])
def login(user: UserCreate):
    if user.email == "admin@admin.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)

# @app.get("/songs_create/{numero}", tags=['songs'])
# async def add_songs(numero: int, session: AsyncSession = Depends(get_session)):
#     for _ in range(numero):  # Generar 10 registros de ejemplo
#         new_song = Song(name=fake.catch_phrase(), artist=fake.name(), year=fake.random_int(min=2000, max=2024))
#         session.add(new_song)
#     await session.commit()
#     return JSONResponse(status_code=201, content={"message": "Se ha agregado canciones: " + str(numero)})

# @app.get("/songs", tags=['songs'], response_model=list[Song])
# async def get_songs(session: AsyncSession = Depends(get_session)):
#     result = await session.execute(select(Song))
#     songs = result.scalars().all()
#     songs_data = [{"name": song.name, "artist": song.artist, "year": song.year, "id": song.id} for song in songs]
#     return JSONResponse(status_code=200, content=songs_data)


# @app.get("/songs/{id}", tags=['songs'], response_model=list[Song])
# async def get_song(id: int, session: AsyncSession = Depends(get_session)):
#     songs = await session.execute(select(Song).where(Song.id==id))
#     song = songs.scalars().first()
#     if song == None:
#         return JSONResponse(status_code=404, content={"message": "Canción no encontrada"})
#     songs_data = [{"name": song.name, "artist": song.artist, "year": song.year, "id": song.id}]
#     return JSONResponse(status_code=200, content=songs_data)

# @app.post("/songs", tags=['songs'])
# async def add_song(song: SongCreate, session: AsyncSession = Depends(get_session)):
#     song = Song(name=song.name, artist=song.artist, year=song.year)
#     session.add(song)
#     await session.commit()
#     await session.refresh(song)
#     return JSONResponse(status_code=201, content={"message": "Se ha registrado la canción"})

# @app.put("/songs/{id}", tags=['songs'])
# async def update_song(id: int, song: SongCreate, session: AsyncSession = Depends(get_session)):
#     song_old = await session.execute(select(Song).where(Song.id==id))
#     song_old = song_old.scalars().first()
#     if song_old == None:
#         return JSONResponse(status_code=404, content={"message": "Canción no encontrada no se puede actualizar"})
#     song_old.name = song.name
#     song_old.artist = song.artist
#     song_old.year = song.year
#     session.add(song_old)
#     await session.commit()
#     return JSONResponse(status_code=200, content={"message": "Se ha modificado la canción"})

# @app.delete("/songs/{id}", tags=['songs'], status_code=201)
# async def delete_song(id: int, session: AsyncSession = Depends(get_session)):
#     songs = await session.execute(select(Song).where(Song.id==id))
#     songs = songs.scalars().first()
#     if songs == None:
#         return JSONResponse(status_code=201, content={"mensaje":"No se encuentra el item a eliminar"})
#     else:
#     # songs = result.scalars().one()
        
#         await session.delete(songs)
#         await session.commit()
#         return JSONResponse(status_code=201, content={"message": "Se ha eliminado la canción"})
    
@app.get("/movies_create/{numero}", tags=['movies'])
async def add_movies(numero: int, session: AsyncSession = Depends(get_session)):
    for _ in range(numero):  # Generar 10 registros de ejemplo
        new_movie = Movie(title=fake.catch_phrase(), overview=fake.catch_phrase(), year=fake.random_int(min=2000, max=2024), rating=fake.random_int(min=1, max=10), category=fake.country())
        session.add(new_movie)
    await session.commit()
    return JSONResponse(status_code=201, content={"message": "Se ha agregado categorias: " + str(numero)})

@app.get("/movies", tags=['movies'], response_model=list[Movie])
async def get_movies(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Movie))
    movies = result.scalars().all()
    movies_data = [{"title": movie.title, "overview": movie.overview, "year": movie.year, "rating": movie.rating, "category": movie.category, "id": movie.id} for movie in movies]
    return JSONResponse(status_code=200, content=movies_data)

@app.get("/movies/{id}", tags=['movies'], response_model=list[Movie])
async def get_movie(id: int, session: AsyncSession = Depends(get_session)):
    movies = await session.execute(select(Movie).where(Movie.id==id))
    movie = movies.scalars().first()
    if movie == None:
        return JSONResponse(status_code=201, content={"mensaje":"No se encuentra el item"})
    movies_data = [{"title": movie.title, "overview": movie.overview, "year": movie.year, "rating": movie.rating, "category": movie.category, "id": movie.id}]
    return JSONResponse(status_code=200, content=movies_data)

@app.post("/movies", tags=['movies'])
async def add_movie(movie: MovieCreate, session: AsyncSession = Depends(get_session)):
    movie = Movie(title=movie.title, overview=movie.overview, year=movie.year, rating=movie.rating, category=movie.category)
    session.add(movie)
    await session.commit()
    await session.refresh(movie)
    return JSONResponse(status_code=201, content={"message": "Se ha registrado una pelicula"})

@app.put("/movies/{id}", tags=['movies'])
async def update_song(id: int, movie: MovieCreate, session: AsyncSession = Depends(get_session)):
    movie_old = await session.execute(select(Movie).where(Movie.id==id))
    movie_old = movie_old.scalars().first()
    if movie_old == None:
        return JSONResponse(status_code=404, content={"message": "Película no encontrada no se puede actualizar"})
    movie_old.title = movie.title
    movie_old.overview = movie.overview
    movie_old.year = movie.year
    movie_old.rating = movie.rating
    movie_old.category = movie.category
    session.add(movie_old)
    await session.commit()
    return JSONResponse(status_code=200, content={"message": "Se ha modificado la película"})

@app.delete("/movies/{id}", tags=['movies'], status_code=201)
async def delete_movie(id: int, session: AsyncSession = Depends(get_session)):
    movie = await session.execute(select(Movie).where(Movie.id==id))
    movie = movie.scalars().first()
    if movie == None:
        return JSONResponse(status_code=404, content={"mensaje":"No se encuentra el item a eliminar"})
    else:
        movies_data = [{"title": movie.title, "overview": movie.overview, "year": movie.year, "rating": movie.rating, "category": movie.category, "id": movie.id}]
        await session.delete(movie)
        await session.commit()
        return JSONResponse(status_code=201, content={"message": "Se ha eliminado la película", "pelicula": movies_data})
