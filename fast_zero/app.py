from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import Message, UserList, UserPublic, UserSchema

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}


@app.get('/html', status_code=HTTPStatus.OK, response_class=HTMLResponse)
def get_html():
    return """
    <html>
        <head>
            <h1>Olá Mundo</h1>
        </head>
    </html>
    """


@app.post('/users', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    """Rota para criar usuário"""

    db_user = session.scalar(
        select(User).where(
            User.username == user.username or User.email == user.email
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username alredy exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists',
            )

    db_user = User(**user.model_dump())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users', response_model=UserList)
def list_users(
    session: Session = Depends(get_session), skip: int = 0, limit: int = 10
):
    """Rota para listar usuários"""
    users = session.scalars(select(User).limit(limit).offset(skip))
    return {'users': users}


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):
    """Rota para atualizar um usuário pelo ID"""
    user_db = session.scalar(
        select(User).where(User.id == user_id)
    )
    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User Not Found'
        )

    user_db.username = user.username
    user_db.email = user.email
    user_db.password = user.password
    session.commit()
    return user_db


@app.delete('/users/{user_id}', response_model=Message)
def deleter_user(user_id: int, session: Session = Depends(get_session)):
    """Rota para deletar um usuário pelo ID"""
    user_db = session.scalar(
        select(User).where(User.id == user_id)
    )
    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User Not Found'
        )

    session.delete(user_db)
    session.commit()

    return {'message': 'User deleted'}


@app.get('/users/{user_id}', response_model=UserPublic)
def get_user(user_id: int, session: Session = Depends(get_session)):
    """Rota para buscar um usuário pelo ID"""
    user_db = session.scalar(
        select(User).where(User.id == user_id)
    )
    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User Not Found'
        )

    return user_db
