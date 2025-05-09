from http import HTTPStatus

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from fast_zero.routers import auth, todos, users
from fast_zero.schemas import Message

app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(todos.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
async def read_root():
    return {'message': 'Olá Mundo!'}


@app.get('/html', status_code=HTTPStatus.OK, response_class=HTMLResponse)
async def get_html():
    return """
    <html>
        <head>
            <h1>Olá Mundo</h1>
        </head>
    </html>
    """
