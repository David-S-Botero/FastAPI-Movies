from fastapi import APIRouter, Path, Query, Body, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List
from schemas.models import Movie
from db_models.movie_db import MovieModel
from middlewares.jwt_bearer import JWTBearer
from config.database import session
from db_models.movie_db import MovieModel 
from services.movie import MovieService

movie_router = APIRouter()

@movie_router.get('/movies', tags=['movies'], response_model=List[Movie], dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    database = session()
    result = MovieService(database).get_movies()
    if not result:
        return JSONResponse(status_code=404, content={"message":"Any movie found."})
    return JSONResponse(status_code=200, content={"movies":jsonable_encoder(result)})
        
@movie_router.get('/movies/{id}', tags=['movies'], response_model=dict, dependencies=[Depends(JWTBearer())])
def get_movie_by_id(id: int = Path(ge=0)) -> dict:
    database = session()
    result = MovieService(database).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={"message":"Any movie found with that id."})
    return JSONResponse(status_code=200, content={"message":"The movie has been found.","movie":jsonable_encoder(result)})
    

@movie_router.get('/movies/', tags=['movies'], response_model=List[Movie])
def get_movies_by_category(category:str = Query(min_length=1, max_length=20)) -> List[Movie]:
    database = session()
    result = MovieService(database).get_movies_by_category(category=category)
    return JSONResponse(status_code=200, content=jsonable_encoder(result)) 


@movie_router.post('/movies', tags=['movies'], response_model=Movie)
def add_movie(movie : Movie = Body()) -> Movie:
    database = session()
    MovieService(database).create_movie(movie=movie)
    return JSONResponse(status_code=200, content={"message" : "Movie added"})
    
@movie_router.delete('/movies', tags=['movies'], response_model=dict)
def delete_movie_by_id(id: int = Query(ge=0))->dict:
    database = session()
    result : MovieModel = MovieService(database).get_movie_by_id(id)
    if not result:
        return JSONResponse(status_code=404,content={"message":"Any movie found with that id."})
    MovieService(database).delete_movie(id)
    return JSONResponse(status_code=200, content={"message":"Movie removed."})

@movie_router.put('/movies/{id}', tags=['movies'], response_model=dict)
def change_all_by_id(id:int = Path(ge=0), movie:Movie = Body()) -> dict:
    database = session()
    result = MovieService(database).get_movie_by_id(id)
    if not result:
        return JSONResponse(status_code=404,content={"message":"Any movie found with that id."})
    MovieService(database).update_movie(id,movie)
    return JSONResponse(status_code=200, content={"message":"Movie changed."})
        

@movie_router.put('/movies/{id}/', tags=['movies'], response_model=dict)
def change_field_by_id(id:int = Path(ge=0), field:str = Query(min_length=1), new_val = Query())->dict:
    database = session()
    result = MovieService(database).get_movie_by_id(id)
    if not result:
        return JSONResponse(status_code=404,content={"message":"Any movie found with that id."})
    serv_result = MovieService(database).change_field_by_id(id=id, field=field, value=new_val)
    if not serv_result:
         return JSONResponse(status_code=404,content={"message":"Category not found or forbid value."})
    return JSONResponse(status_code=200, content={"message":"Movie changed."})
    