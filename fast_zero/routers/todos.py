from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import Todo, User
from fast_zero.schemas import (
    FilterTodo,
    TodoList,
    TodoPublic,
    TodoSchema,
    TodoUpdate,
)
from fast_zero.security import get_curret_user

router = APIRouter(prefix='/todos', tags=['todos'])

T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_curret_user)]


@router.post('', response_model=TodoPublic)
async def create_todo(
    todo: TodoSchema, session: T_Session, user: T_CurrentUser
):
    """Rota para criar uma todo"""

    todo_db = Todo(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        user_id=user.id,
    )

    session.add(todo_db)
    await session.commit()
    await session.refresh(todo_db)

    return todo_db


@router.get('', response_model=TodoList)
async def read_todos(
    session: T_Session,
    current_user: T_CurrentUser,
    filter_query: Annotated[FilterTodo, Query()],
):
    """Rota para listar todos os todos do usuário logado"""

    query = select(Todo).where(Todo.user_id == current_user.id)

    if filter_query.title:
        query = query.filter(Todo.title.contains(filter_query.title))

    if filter_query.description:
        query = query.filter(
            Todo.description.contains(filter_query.description)
        )

    if filter_query.state:
        query = query.filter(Todo.state == filter_query.state)

    todos = await session.scalars(
        query.offset(filter_query.offset).limit(filter_query.limit)
    )

    return {'todos': todos.all()}


@router.patch('/{todo_id}', response_model=TodoPublic)
async def update_todo(
    todo_id: int, session: T_Session, user: T_CurrentUser, todo: TodoUpdate
):
    """Rota para atualizar uma todo"""
    todo_db = await session.scalar(
        select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id)
    )

    if not todo_db:
        raise HTTPException(
            detail='Todo not found',
            status_code=HTTPStatus.NOT_FOUND,
        )

    for key, value in todo.model_dump(exclude_unset=True).items():
        setattr(todo_db, key, value)

    session.add(todo_db)
    await session.commit()
    await session.refresh(todo_db)

    return todo_db


@router.delete('/{todo_id}')
async def delete_todo(
    todo_id: int,
    session: T_Session,
    user: T_CurrentUser,
):
    """Roota para deletar uma todo"""
    todo_db = await session.scalar(
        select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id)
    )

    if not todo_db:
        raise HTTPException(
            detail='Todo not found',
            status_code=HTTPStatus.NOT_FOUND,
        )

    await session.delete(todo_db)
    await session.commit()

    return {'message': 'Todo deleted'}
