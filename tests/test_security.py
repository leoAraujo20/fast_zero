from jwt import decode

from fast_zero.security import create_access_token, settings


def test_create_jwt_token():
    data = {'sub': 'test_user'}
    token = create_access_token(data)

    decoded_data = decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )

    assert decoded_data['sub'] == 'test_user'
    assert 'exp' in decoded_data
