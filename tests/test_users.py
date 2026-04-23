from http import HTTPStatus

from fast_zero.schemas import UserPublic


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


def test_create_user_error_email(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'Teste1',
            'email': 'teste@test.com',
            'password': 'testtest',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already exists'}


def test_create_user_error_username(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'Teste',
            'email': 'tes@te.com',
            'password': 'testtest',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already exists'}


def test_read_users(client):
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.json() == {'users': [user_schema]}


def test_read_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/1')

    assert response.json() == user_schema


def test_read_user_error(client, user):
    response = client.get('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'USER NOT FOUND'}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'usernameteste2',
            'email': 'teste@teste.com',
            'password': '123',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'usernameteste2',
        'email': 'teste@teste.com',
        'id': user.id,
    }


def test_update_user_error(client, user, token):
    response = client.put(
        '/users/9999',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'usernameteste2',
            'email': 'teste@teste.com',
            'password': '123',
            'id': 1,
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_update_integrity_error(client, user, token):
    # Inserindo fausto
    client.post(
        '/users',
        json={
            'username': 'Henrique',
            'email': 'henri@que.com',
            'password': 'secret',
        },
    )

    # Alterando o user das fixture para fausto
    response_update = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'Henrique',
            'email': 'Henri@que.com',
            'password': 'mynewpassword',
        },
    )

    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {
        'detail': 'Username or Email already exists'
    }


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_error(client, user, token):
    response = client.delete(
        '/users/9999', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}
