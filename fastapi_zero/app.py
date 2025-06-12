from http import HTTPStatus

from fastapi import FastAPI

from fastapi_zero.routers import auth, user
from fastapi_zero.schemas import Message

app = FastAPI(title='FastAPI Zero - Curso FastAPI', version='0.1.0')
app.include_router(auth.router)
app.include_router(user.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Hello World'}
