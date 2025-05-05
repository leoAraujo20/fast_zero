from http import HTTPStatus

from fast_zero.schemas import UserPublic
from fast_zero.security import create_access_token


def test_create_user(client):
    response = client.post(
        '/users',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )

    assert response.json() == {
        'id': 1,
        'username': 'alice',
        'email': 'alice@example.com',
    }


def test_create_user_with_existing_username(client, user):
    response = client.post(
        '/users',
        json={
            'username': f'{user.username}',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_with_existing_email(client, user):
    response = client.post(
        '/users',
        json={
            'username': 'alice',
            'email': f'{user.email}',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'E-mail already exists'}


def test_read_users(client, user):
    response = client.get('/users')
    user_schema = UserPublic.model_validate(user).model_dump()

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_read_one_user(client, user):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == UserPublic.model_validate(user).model_dump()


def test_read_one_user_should_return_not_found(client, user):
    response = client.get('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User Not Found'}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user.id,
        'username': 'bob',
        'email': 'bob@example.com',
    }


def test_update_user_should_return_conflict(client, user, other_user, token):
    response = client.put(
        f'users/{other_user.id}',
        json={
            'username': 'test',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permission'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_should_return_unauthorized(
    client, user, other_user, token
):
    response = client.delete(
        f'users/{other_user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permission'}


def test_get_current_user_with_invalid_token(client):
    data = {'no-username': 'test'}
    token = create_access_token(data)

    response = client.delete(
        'users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_does_not_exist(client):
    data = {'sub': 'test'}
    token = create_access_token(data)

    response = client.delete(
        'users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
