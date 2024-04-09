from fastapi import  FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer
from fastapi.encoders import jsonable_encoder


from app.db import get_session, init_db
from app.models import Song, SongCreate, Movie, MovieCreate, UserCreate
from app.error_handler import ErrorHandler
from app.jwt_bearer import create_token, validate_token
from app.routers_movies import movie_router
from app.routers_users import user_router

app = FastAPI()
app.title = "Mi aplicación con  FastAPI"
app.version = "0.0.1"
app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(user_router)
# descomentar para crear la base de datos
# @app.on_event("startup")
# async def on_startup():
#     init_db()

@app.get('/', tags=['home'])

def message():
    return HTMLResponse('<h1>Bienvenido a fastapi</h1>')
