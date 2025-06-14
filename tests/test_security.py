from http import HTTPStatus

from jwt import decode

from fastapi_zero.security import create_access_token


def test_jwt(settings):
    data = {'test': 'test'}

    token = create_access_token(data)

    decoded = decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )

    assert decoded['test'] == data['test']
    assert 'exp' in decoded


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer invalid_token'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_missing_sub_in_token(client, settings, user):
    token_data_without_sub = {'some_other_claim': 'some_value'}
    access_token = create_access_token(token_data_without_sub)

    response = client.delete(
        f'/users/{user.id}/',
        headers={'Authorization': f'Bearer {access_token}'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_non_existent_user(client, settings, user):
    token_data = {'sub': 'nonexistentuser@example.com'}
    access_token = create_access_token(token_data)

    response = client.delete(
        f'/users/{user.id}/',
        headers={'Authorization': f'Bearer {access_token}'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
