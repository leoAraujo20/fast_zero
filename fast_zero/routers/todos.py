from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import Todo, User
from fast_zero.schemas import TodoPublic, TodoSchema
from fast_zero.security import get_curret_user

router = APIRouter(prefix='/todos', tags=['todos'])

T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_curret_user)]


@router.post('/create', response_model=TodoPublic)
async def create_todo(
    todo: TodoSchema, session: T_Session, user: T_CurrentUser
):
    """Rota para criar um todo"""

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
