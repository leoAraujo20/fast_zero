from http import HTTPStatus


def test_root_return_ok_hello_world(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_should_return_html(client):
    response = client.get('/html')

    assert response.status_code == HTTPStatus.OK
    assert '<h1>Olá Mundo</h1>' in response.text
