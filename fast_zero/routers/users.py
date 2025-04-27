from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import Message, UserList, UserPublic, UserSchema
from fast_zero.security import get_curret_user, get_password_hash

router = APIRouter(prefix='/users', tags=['users'])
T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_curret_user)]


@router.get('', response_model=UserList)
def list_users(
    session: T_Session,
    skip: int = 0,
    limit: int = 10,
):
    """Rota para listar usuários"""
    users = session.scalars(select(User).limit(limit).offset(skip))
    return {'users': users}


@router.put('/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int,
    user: UserSchema,
    session: T_Session,
    current_user: T_CurrentUser,
):
    """Rota para atualizar um usuário pelo ID"""
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permission'
        )

    current_user.username = user.username
    current_user.email = user.email
    current_user.password = get_password_hash(user.password)
    session.commit()
    session.refresh(current_user)
    return current_user


@router.delete('/{user_id}', response_model=Message)
def deleter_user(
    user_id: int,
    session: T_Session,
    current_user: T_CurrentUser,
):
    """Rota para deletar um usuário pelo ID"""
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permission'
        )

    session.delete(current_user)
    session.commit()

    return {'message': 'User deleted'}


@router.get('/{user_id}', response_model=UserPublic)
def get_user(user_id: int, session: T_Session):
    """Rota para buscar um usuário pelo ID"""
    user_db = session.scalar(select(User).where(User.id == user_id))
    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User Not Found'
        )

    return user_db


@router.post('', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: T_Session):
    """Rota para criar usuário"""
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='E-mail already exists',
            )

    db_user = User(
        username=user.username,
        password=get_password_hash(user.password),
        email=user.email,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user
