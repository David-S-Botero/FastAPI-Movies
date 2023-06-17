import json
from models import Movie

def read_data()->list:
    with open("db/data.json") as f:
        data = json.load(f)
        data = [Movie(id=item["id"], title=item["title"], overview=item["overview"], year=item["year"], rating=item["rating"], category=item["category"]) for item in data]
    return data

def add_data(model, del_data=False):
    
    if del_data:
        model_json = list(map(
            lambda i :{
                "id" : i.id,
                "title" : i.title,
                "overview" : i.overview,
                "year" : i.year,
                "category" : i.category,
                "rating" : i.rating
                }, model))   
        with open("db/data.json","w") as f:
            json.dump(model_json,f,indent=6,ensure_ascii=False)
    else:
        txt = read_data()
        txt.append(model)
        model_json = list(map(
            lambda i :{
                "id" : i.id,
                "title" : i.title,
                "overview" : i.overview,
                "year" : i.year,
                "category" : i.category,
                "rating" : i.rating
                }, txt))   
        with open("db/data.json","w") as f:
            json.dump(model_json,f,indent=6,ensure_ascii=False)
