from http import HTTPStatus

from jwt import decode

from fast_zero.security import ALGORITHM, SECRET_KEY, create_acess_token


def test_create_jwt_token():
    data = {'sub': 'test_user'}
    token = create_acess_token(data)

    decoded_data = decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert decoded_data['sub'] == 'test_user'
    assert 'exp' in decoded_data


def test_get_current_user_with_invalid_token(client):
    data = {'no-username': 'test'}
    token = create_acess_token(data)

    response = client.delete(
        'users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_does_not_exist(client):
    data = {'sub': 'test'}
    token = create_acess_token(data)

    response = client.delete(
        'users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
