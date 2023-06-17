from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import db
import copy
from models.models import Movie

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
        if i.id == id:
            return i
    return {}

@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category:str):
    movies = list(filter(lambda x:x.category==category, db.read_data()))
    return movies

@app.post('/movies', tags=['movies'])
def add_movie(movie : Movie):
    db.add_data(movie)
    return movie
    
@app.delete('/movies', tags=['movies'])
def delete_movie_by_id(id: int):
    movies = db.read_data()
    new_movies = [item for item in movies if item.id !=id]
    db.add_data(new_movies,del_data=True)
    return new_movies

@app.put('/movies/{id}', tags=['movies'])
def change_all_by_id(id:int, movie : Movie):
    data = db.read_data()
    if len([item for item in data if item.id==id]) != 0:
        register_changed = copy.deepcopy(movie)
        register_changed.id = id
        for i, item in enumerate(data):
            if item.id==id:
                data[i]=register_changed
        db.add_data(data, True)
        return register_changed
    else:
        return {}

@app.put('/movies/{id}/', tags=['movies'])
def change_field_by_id(id:int, field:str, new_val):
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
            return register_changed
        else:
            return 'no field in atributes'
    else:
        return {}
    
data = db.read_data()
for i, item in enumerate(data):
    print(item)
    if item.id==2:
        data[i]=Movie(2,"string", "string", "string", 3.2, "string")
print(data)
    
