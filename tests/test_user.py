from http import HTTPStatus

from fastapi_zero.schemas import UserPublic

NUMBER_OF_USERS_CREATED = 2


def test_create_user(client):
    response = client.post(
        '/users',
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


def test_read_user_by_id_not_found(client, token):
    response = client.get(
        '/users/666/', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_read_user_by_id_success(client, user, token):
    response = client.get(
        f'/users/{user.id}/', headers={'Authorization': f'Bearer {token}'}
    )

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
    response = client.delete(
        f'/users/{user.id}/', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'User deleted',
    }


def test_update_user_permission_denied(client, other_user, token):
    response = client.put(
        f'/users/{other_user.id}/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_delete_user_permission_denied(client, other_user, token):
    response = client.delete(
        f'/users/{other_user.id}/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_update_integrity_error(client, user, token):
    client.post(
        '/users/',
        json={
            'username': 'fausto',
            'email': 'fausto@example.com',
            'password': 'secret',
        },
    )

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


def test_read_users_empty_list_with_offset(client, user, token):
    response = client.get(
        '/users/?limit=10&offset=5',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}
