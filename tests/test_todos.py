import factory
import factory.fuzzy
import pytest

from fast_zero.models import Todo, TodoState


class TodoFactory(factory.Factory):
    class Meta:
        model = Todo

    title = factory.Faker('text')
    description = factory.Faker('text')
    state = factory.fuzzy.FuzzyChoice(TodoState)
    user_id = 1


def test_create_todo(client, user, token):
    response = client.post(
        '/todos/create',
        json={
            'title': 'Test Todo',
            'description': 'This is a test todo',
            'state': 'todo',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.json() == {
        'id': 1,
        'title': 'Test Todo',
        'description': 'This is a test todo',
        'state': 'todo',
    }


@pytest.mark.asyncio
async def test_read_todos(session, client, user, token):
    expected_todos = 5
    session.add_all(
        TodoFactory.build_batch(expected_todos, user_id=user.id)
    )

    await session.commit()

    response = client.get(
        '/todos',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_read_todos_with_pagination(
    session, client, user, token
):
    expected_todos = 2
    session.add_all(
        TodoFactory.build_batch(5, user_id=user.id)
    )

    await session.commit()
    response = client.get(
        '/todos',
        headers={'Authorization': f'Bearer {token}'},
        params={'offset': 1, 'limit': expected_todos},
    )

    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_read_todos_with_filter_title(
    session, client, user, token
):
    expected_todos = 5
    session.add_all(
        TodoFactory.build_batch(5, title='Test Title', user_id=user.id)
    )

    await session.commit()
    response = client.get(
        '/todos',
        headers={'Authorization': f'Bearer {token}'},
        params={'title': 'Test Title'},
    )

    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_read_todos_with_filter_description(
    session, client, user, token
):
    expected_todos = 5
    session.add_all(
        TodoFactory.build_batch(
            5, description='Test Description', user_id=user.id
        )
    )

    await session.commit()
    response = client.get(
        '/todos',
        headers={'Authorization': f'Bearer {token}'},
        params={'description': 'Test Description'},
    )

    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_read_todos_with_filter_state(
    session, client, user, token
):
    expected_todos = 5
    session.add_all(
        TodoFactory.build_batch(5, state=TodoState.done, user_id=user.id)
    )

    await session.commit()
    response = client.get(
        '/todos',
        headers={'Authorization': f'Bearer {token}'},
        params={'state': 'done'},
    )

    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_read_todos_with_all_filters(
    session, client, user, token
):
    expected_todos = 5
    session.add_all(
        TodoFactory.build_batch(
            5,
            title='Test Title',
            description='Test Description',
            state=TodoState.done,
            user_id=user.id,
        )
    )

    session.add_all(
        TodoFactory.create_batch(
            3,
            user_id=user.id,
            title='Other title',
            description='other description',
            state=TodoState.todo,
        )
    )

    await session.commit()
    response = client.get(
        '/todos',
        headers={'Authorization': f'Bearer {token}'},
        params={
            'title': 'Test Title',
            'description': 'Test Description',
            'state': 'done',
        },
    )

    assert len(response.json()['todos']) == expected_todos
