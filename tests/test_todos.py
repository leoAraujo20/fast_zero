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
