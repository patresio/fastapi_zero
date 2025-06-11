from http import HTTPStatus

from fastapi_zero.schemas import UserPublic


# Exercicio 01 - Aula 02
def test_exercicio_ola_mundo_em_html(client):
    response = client.get('/html')
    assert response.status_code == HTTPStatus.OK
    assert '<h1> Olá Mundo </h1>' in response.text


def test_read_root(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello World'}


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


def test_create_user_with_existing_username(client, user):
    response = client.post(
        '/users/',
        json={
            'username': user.username,
            'email': 'newemail@example.com',
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already registered'}


def test_create_user_with_existing_email(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'newuser',
            'email': user.email,
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already registered'}


def test_read_users(client, user, token):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get(
        '/users/', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


# Exercicio 03 - Aula 03
def test_get_user_should_return_not_found__exercicio(client, user, token):
    response = client.get(
        '/users/666/', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_get_user___exercicio(client, user, token):
    response = client.get(
        f'/users/{user.id}/', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': user.username,
        'email': user.email,
        'id': user.id,
    }


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}/',
        headers={'Authorization': f'Bearer {token}'},
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
        'id': user.id,
    }


def test_delete_user(client, user, token):
    response = client.delete(f'/users/{user.id}/', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'User deleted',
    }


# --- Exercicios das aulas ---


# Exercicio 01 - Aula 03
def test_update_user_should_return_not_found__exercicio(client, user, token):
    response = client.put(
        '/users/123/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


# Exercicio 02 - Aula 03
def test_delete_user_should_return_not_found__exercicio(client, user, token):
    response = client.delete(
        '/users/123/', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_update_integrity_error(client, user, token):
    # inserindo fausto
    client.post(
        '/users/',
        json={
            'username': 'fausto',
            'email': 'fausto@example.com',
            'password': 'secret',
        },
    )

    # Alterando o user das fixtures para fausto
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'fausto',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username or email already exists'}


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={
            'username': user.email,
            'password': user.clean_password,
        },
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token
