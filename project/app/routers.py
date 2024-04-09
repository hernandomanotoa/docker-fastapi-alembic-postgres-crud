from fastapi import APIRouter
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
from app.models import Movie
from app.services import MovieService
from app.jwt_bearer import JWTBearer

movie_router = APIRouter()
fake = Faker()
@movie_router.get("/movies_create/{numero}", tags=['movies'])
async def add_movies(numero: int, session: AsyncSession = Depends(get_session)):
    for _ in range(numero):  # Generar 10 registros de ejemplo
        new_movie = Movie(title=fake.catch_phrase(), overview=fake.catch_phrase(), year=fake.random_int(min=2000, max=2024), rating=fake.random_int(min=1, max=10), category=fake.country())
        session.add(new_movie)
    await session.commit()
    return JSONResponse(status_code=201, content={"message": "Se ha agregado categorias: " + str(numero)})

@movie_router.get("/movies", tags=['movies'], response_model=list[Movie])
async def get_movies(session: AsyncSession = Depends(get_session)):
    movies = await MovieService(session).get_movies()
    # movies_data = [{"title": movie.title, "overview": movie.overview, "year": movie.year, "rating": movie.rating, "category": movie.category, "id": movie.id} for movie in movies]
    movies_data = [movie.dict() for movie in movies]
    return JSONResponse(status_code=200, content=movies_data)

@movie_router.get("/movies/{id}", tags=['movies'], response_model=list[Movie])
async def get_movie(id: int, session: AsyncSession = Depends(get_session)):
    movie = await MovieService(session).get_movie(id)
    if movie == None:
        return JSONResponse(status_code=201, content={"mensaje":"No se encuentra el item"})
    # movies_data = [{"title": movie.title, "overview": movie.overview, "year": movie.year, "rating": movie.rating, "category": movie.category, "id": movie.id}]
    movies_data = [movie.dict()]
    return JSONResponse(status_code=200, content=movies_data)

@movie_router.post("/movies", tags=['movies'])
async def add_movie(movie: MovieCreate, session: AsyncSession = Depends(get_session)):
    await MovieService(session).create_movie(movie)
    return JSONResponse(status_code=201, content={"message": "Se ha registrado una pelicula"})

@movie_router.put("/movies/{id}", tags=['movies'])
async def update_song(id: int, movie: MovieCreate, session: AsyncSession = Depends(get_session)):
    movie_old = await MovieService(session).get_movie(id)
    if movie_old == None:
        return JSONResponse(status_code=404, content={"message": "Película no encontrada no se puede actualizar"})
    
    await MovieService(session).update_movie(id, movie)
    return JSONResponse(status_code=200, content={"message": "Se ha modificado la película"})

@movie_router.delete("/movies/{id}", tags=['movies'], status_code=201)
async def delete_movie(id: int, session: AsyncSession = Depends(get_session)):
    movie_old = await MovieService(session).get_movie(id)
    if movie_old == None:
        return JSONResponse(status_code=404, content={"mensaje":"No se encuentra el item a eliminar"})
    else:
        # movies_data = [{"title": movie.title, "overview": movie.overview, "year": movie.year, "rating": movie.rating, "category": movie.category, "id": movie.id}]
        movie_old = await MovieService(session).delete_movie(id)
        return JSONResponse(status_code=201, content={"message": "Se ha eliminado la película"})