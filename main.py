from fastapi import FastAPI, Body, Response
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
    
@app.delete('/movies', tags=['movies'])
def delete_movie_by_id(id: int):
    movies = db.read_data()
    new_movies = [item for item in movies if item["id"]!=id]
    db.add_data(new_movies,del_data=True)
    return new_movies

@app.put('/movies/{id}', tags=['movies'])
def change_all_by_id(id:int, title:str = Body(), overview:str = Body(), year:str = Body(),
               category:str = Body(), rating:float = Body()):
    data = db.read_data()
    register_changed = [item for item in data if item["id"]==id][0]
    register_changed["title"] = title
    register_changed["overview"] = overview
    register_changed["year"] = year
    register_changed["category"] = category
    register_changed["rating"] = rating
    for item in data:
        if item["id"]==id:
            item=register_changed
    db.add_data(data, True)
    return register_changed

@app.put('/movies/{id}/', tags=['movies'])
def change_field_by_id(id:int, field:str, new_val):
    data = db.read_data()
    register_changed = [item for item in data if item["id"]==id][0]
    if field.lower() in register_changed.keys():
        register_changed[field.lower()]=new_val
        for item in data:
            if item["id"]==id:
                item=register_changed
        db.add_data(data, True)
    return register_changed
    
    

    
