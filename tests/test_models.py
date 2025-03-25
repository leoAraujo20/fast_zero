from sqlalchemy import select

from fast_zero.models import User


def test_user_model(session):
    new_user = User(username='test', password='test', email='test@gmail.com')

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    user = session.scalar(select(User).where(User.username == 'test'))

    assert user.id == 1
