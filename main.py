from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.user import user_router
import uvicorn
import os

app = FastAPI()

app.title = "My app with FastAPI"
app.version = "0.0.1"

app.add_middleware(ErrorHandler)

app.include_router(movie_router)
app.include_router(user_router)

Base.metadata.create_all(bind=engine)

@app.get('/', tags=['home'], response_model=str)
def message() -> str:
    return HTMLResponse('<h1>Hello World!</h1>')

if __name__ == '__main__':

    uvicorn.run('main:app', host="0.0.0.0")
    port = int(os.environ.get('PORT', 8000))