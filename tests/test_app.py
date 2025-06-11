from http import HTTPStatus


def test_read_root(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello World'}


# --- Exercicios das aulas ---


# Exercicio 01 - Aula 02
def test_exercicio_ola_mundo_em_html(client):
    response = client.get('/html')
    assert response.status_code == HTTPStatus.OK
    assert '<h1> Olá Mundo </h1>' in response.text


# Exercicio 01 - Aula 03
def test_update_user_should_return_not_found__exercicio(client):
    response = client.put(
        '/users/666',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}

# --- Outros Teste ---


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_read_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'username': 'alice',
                'email': 'alice@example.com',
                'id': 1,
            }
        ]
    }


def test_update_user(client):
    response = client.put(
        '/users/1/',
        json={
            'username': 'bobs',
            'email': 'bobs@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bobs',
        'email': 'bobs@example.com',
        'id': 1,
    }


def test_delete_user(client):
    response = client.delete('/users/1/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bobs',
        'email': 'bobs@example.com',
        'id': 1,
    }
