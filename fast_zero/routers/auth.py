from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import Token
from fast_zero.security import (
    create_access_token,
    get_curret_user,
    verify_password,
)

router = APIRouter(prefix='/auth', tags=['auth'])
T_Session = Annotated[AsyncSession, Depends(get_session)]
T_Oauth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
T_CurrentUser = Annotated[User, Depends(get_curret_user)]


@router.post('/token', response_model=Token)
async def login_for_acess_token(
    session: T_Session,
    form_data: T_Oauth2Form,
):
    user = await session.scalar(
        select(User).where(User.username == form_data.username)
    )

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect username or password',
        )

    access_token = create_access_token(data={'sub': user.username})

    return {'access_token': access_token, 'token_type': 'Bearer'}


@router.post('/refresh_token', response_model=Token)
async def refresh_token(
    current_user: T_CurrentUser,
):
    token = create_access_token(data={'sub': current_user.username})
    return {'access_token': token, 'token_type': 'Bearer'}
