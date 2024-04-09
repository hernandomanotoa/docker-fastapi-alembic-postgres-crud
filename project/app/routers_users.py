from fastapi import APIRouter
from fastapi import Depends, FastAPI, Body, HTTPException, Path, Query, Request
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer
from fastapi.encoders import jsonable_encoder
from faker import Faker

from app.db import get_session, init_db
from app.models import User, UserCreate
from app.error_handler import ErrorHandler
from app.jwt_bearer import create_token, validate_token
from app.models import User
from app.services_users import UserService
from app.jwt_bearer import JWTBearer



user_router = APIRouter()
fake = Faker()

@user_router.post('/login', tags=['auth'])
async def login(user: UserCreate, session: AsyncSession = Depends(get_session)):
    user_login = await UserService(session).get_users_by_email_password(user)
    if user_login == None:
        return JSONResponse(status_code=201, content={"mensaje":"Datos de login incorrectos"})
    
    if user.email == user_login.email and user.password == user_login.password:
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)

@user_router.get("/users_create/{numero}", tags=['users'])
async def add_users(numero: int, session: AsyncSession = Depends(get_session)):
    for _ in range(numero):
        new_user = User(email=(fake.name()).lower().replace(' ', '.')+"@.correo.com", password="admin")
        session.add(new_user)
    await session.commit()
    return JSONResponse(status_code=201, content={"message": "Se ha agregado usuarios: " + str(numero)})

@user_router.get("/users", tags=['users'], response_model=list[User])
async def get_users(session: AsyncSession = Depends(get_session)):
    users = await UserService(session).get_users()
    users_data = [user.dict() for user in users]
    return JSONResponse(status_code=200, content=users_data)

@user_router.get("/users/{id}", tags=['users'], response_model=list[User])
async def get_user(id: int, session: AsyncSession = Depends(get_session)):
    user = await UserService(session).get_user(id)
    if user == None:
        return JSONResponse(status_code=201, content={"mensaje":"No se encuentra el item"})
    users_data = [user.dict()]
    return JSONResponse(status_code=200, content=users_data)

@user_router.post("/users", tags=['users'], dependencies=[Depends(JWTBearer())])
async def add_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    await UserService(session).create_user(user)
    return JSONResponse(status_code=201, content={"message": "Se ha registrado una usuario"})

@user_router.put("/users/{id}", tags=['users'], dependencies=[Depends(JWTBearer())])
async def update_song(id: int, user: UserCreate, session: AsyncSession = Depends(get_session)):
    user_old = await UserService(session).get_user(id)
    if user_old == None:
        return JSONResponse(status_code=404, content={"message": "Usuario no encontrada no se puede actualizar"})
    
    await UserService(session).update_user(id, user)
    return JSONResponse(status_code=200, content={"message": "Se ha modificado la usuario"})

@user_router.delete("/users/{id}", tags=['users'], status_code=201, dependencies=[Depends(JWTBearer())])
async def delete_user(id: int, session: AsyncSession = Depends(get_session)):
    user_old = await UserService(session).get_user(id)
    if user_old == None:
        return JSONResponse(status_code=404, content={"mensaje":"No se encuentra el item a eliminar"})
    else:
        user_old = await UserService(session).delete_user(id)
        return JSONResponse(status_code=201, content={"message": "Se ha eliminado la usuario"})