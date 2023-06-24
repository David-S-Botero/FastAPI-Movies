from fastapi import FastAPI, Path, Query, Body, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from typing import List
import db
import copy
from models import *
from jwt_manager import create_token, JWTBearer

app = FastAPI()

app.title = "My app with FastAPI"
app.version = "0.0.1"

@app.get('/', tags=['home'], response_model=str)
def message() -> str:
    return HTMLResponse('<h1>Hello World!</h1>')

@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    return db.read_data()

@app.get('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def get_movie_by_id(id: int = Path(ge=0)) -> dict:
    for movie in db.read_data():
        if movie.id == id:
            return {"message":"The movie has been found.","Movie":movie}
    return {"message":"Any movie found with that id."}

@app.get('/movies/', tags=['movies'], response_model=List[Movie], status_code=200)
def get_movies_by_category(category:str = Path(min_length=1, max_length=20)) -> List[Movie]:
    movies = list(filter(lambda x:x.category==category, db.read_data()))
    return movies

@app.post('/movies', tags=['movies'], response_model=Movie, status_code=200)
def add_movie(movie : Movie = Body()) -> Movie:
    db.add_data(movie)
    return movie
    
@app.delete('/movies', tags=['movies'], response_model=dict, status_code=200)
def delete_movie_by_id(id: int = Path(ge=0))->dict:
    movies = db.read_data()
    new_movies = [item for item in movies if item.id !=id]
    if len(new_movies) != 0:
        db.add_data(new_movies,del_data=True)
        return {"message":"The movie has been deleted."}
    else:
        return {"message":"Any movie found with that id."}

@app.put('/movies/{id}', tags=['movies'], response_model=dict)
def change_all_by_id(id:int = Path(ge=0), movie:Movie = Body()) -> dict:
    data = db.read_data()
    if len([item for item in data if item.id==id]) != 0:
        register_changed = copy.deepcopy(movie)
        register_changed.id = id
        for i, item in enumerate(data):
            if item.id==id:
                data[i]=register_changed
        db.add_data(data, True)
        return {"message":"The movie has been changed.","Changes":register_changed}
    else:
        return {"message":"Any movie found with that id."}

@app.put('/movies/{id}/', tags=['movies'], response_model=dict)
def change_field_by_id(id:int = Path(ge=0), field:str = Query(min_length=1), new_val = Query())->dict:
    field = field.lower()
    data = db.read_data()
    compat_registers = [item for item in data if item.id==id]
    if len(compat_registers)!=0:
        register_changed = compat_registers[0]
        attributes = [item for item in dir(register_changed) if '__' not in item]
        if field in attributes:
            model_json = {
                "id" : register_changed.id,
                "title" : register_changed.title,
                "overview" : register_changed.overview,
                "year" : register_changed.year,
                "category" : register_changed.category,
                "rating" : register_changed.rating
            }
            model_json[attributes[attributes.index(field)]]=new_val
            register_changed = Movie(id=model_json['id'],title=model_json['title'],
                                     overview=model_json['overview'],year=model_json['year'],
                                     rating=model_json['rating'], category=model_json['category'])
            for i, item in enumerate(data):
                if item.id==id:
                    data[i]=register_changed
            db.add_data(data, True)
            return {"message":"The movie has been changed.","Changes":register_changed}
        else:
            return {"message":"Attribute not found."}
    else:
        return {"message":"Any movie found with that id."}
    
    
@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token:str = create_token(user.__dict__)
        return JSONResponse(content=token, status_code=200)
    else:
        return JSONResponse(content={"message":"The data don't match."},status_code=404)