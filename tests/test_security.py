from jwt import decode

from fast_zero.security import ALGORITHM, SECRET_KEY, create_acess_token


def test_create_jwt_token():
    data = {'sub': 'test_user'}
    token = create_acess_token(data)

    decoded_data = decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert decoded_data['sub'] == 'test_user'
    assert 'exp' in decoded_data
