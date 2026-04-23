from http import HTTPStatus


def test_read_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')  # Act (Ação)

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'Olá Mundo!'}  # Assert


def test_exercicio_aula_02_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/html')  # Act (Ação)

    assert response.status_code == HTTPStatus.OK  # Assert
    assert '<h1>Olá Mundo!</h1>' in response.text  # Assert
