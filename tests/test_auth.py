from http import HTTPStatus


def test_create_access_token(client, user):
    response = client.post(
        '/auth/token',
        data={
            'username': user.username,
            'password': user.clean_password,
        },
    )

    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token


def test_login_for_access_token_with_invalid_credentials(client, user):
    response = client.post(
        '/auth/token',
        data={
            'username': user.username,
            'password': 'wrongpassword',
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect username or password'}
