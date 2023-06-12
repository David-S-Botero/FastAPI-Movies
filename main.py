from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
import db 

app = FastAPI()

app.title = "My app with FastAPI"
app.version = "0.0.1"

@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello World!</h1>')

@app.get('/movies', tags=['movies'])
def get_movies():
    return db.read_data()

@app.get('/movies/{id}', tags=['movies'])
def get_movies_by_id(id: int):
    for i in db.read_data():
        if i["id"] == id:
            return i
    return {}

@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category:str):
    movies = list(filter(lambda x:x['category']==category, db.read_data()))
    return movies

@app.post('/movies', tags=['movies'])
def add_movie(id:int = Body(), title:str = Body(), overview:str = Body(), year:str = Body(),
               category:str = Body(), rating:float = Body()):
    register = {
                "id":id,
                "title":title,
                "overview":overview,
                "year":year,
                "category":category,
                "rating":rating
            }
    db.add_data(register)
    return register
    