from http import HTTPStatus


def test_read_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')  # Act (Ação)

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'Olá Mundo!'}  # Assert


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'usernameteste',
            'password': '1234',
            'email': 'teste@teste.com',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'usernameteste',
        'email': 'teste@teste.com',
    }


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {'id': 1, 'username': 'usernameteste', 'email': 'teste@teste.com'}
        ]
    }


def test_read_user(client):
    response = client.get('/users/1')

    assert response.json() == {
        'id': 1,
        'username': 'usernameteste',
        'email': 'teste@teste.com',
    }


def test_read_user_error(client):
    response = client.get('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'USER NOT FOUND'}


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'usernameteste2',
            'email': 'teste@teste.com',
            'password': '123',
            'id': 1,
        },
    )

    assert response.json() == {
        'username': 'usernameteste2',
        'email': 'teste@teste.com',
        'id': 1,
    }


def test_update_user_error(client):
    response = client.put(
        '/users/2',
        json={
            'username': 'usernameteste2',
            'email': 'teste@teste.com',
            'password': '123',
            'id': 1,
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'USER NOT FOUND'}


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.json() == {'message': 'User Deleted'}


def test_delete_user_error(client):
    response = client.delete('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'USER NOT FOUND'}


def test_exercicio_aula_02_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/html')  # Act (Ação)

    assert response.status_code == HTTPStatus.OK  # Assert
    assert '<h1>Olá Mundo!</h1>' in response.text  # Assert
