import datetime
from db_models.movie_db import MovieModel
from schemas.models import Movie

class MovieService():

    def __init__(self,db) -> None:
        self.db = db

    def get_movies(self):
        result = self.db.query(MovieModel).all()
        return result
    
    def get_movie_by_id(self, id:int):
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        return result
    
    def get_movies_by_category(self, category:str):
        result = self.db.query(MovieModel).where(MovieModel.category == category).all()
        return result
    
    def create_movie(self, movie:Movie):
        new_movie = MovieModel(**movie.dict())
        self.db.add(new_movie)
        self.db.commit()
        return
    
    def update_movie(self, id:int, movie:Movie):
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        result.category = movie.category
        result.overview = movie.overview
        result.rating = movie.rating
        result.title = movie.title
        result.year = movie.year
        self.db.commit()
        return
    
    def delete_movie(self, id:int) -> None:
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        self.db.delete(result)
        self.db.commit()
        return
    
    def change_field_by_id(self, id:int, field:str, value) -> bool:
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        field = field.lower()
        if(field == 'title'):
            result.title = value
        elif(field == 'category'):
            result.category = value
        elif(field == 'rating'):
            if not value.isnumeric():
                return False
            value = float(value)
            if value < 0:
                return False
            result.rating = value
        elif(field == 'year'):
            if not value.isdigit():
                return False
            value = int(value)
            if value > datetime.date.today().year or value <= 0:
                return False
            result.year = value
        elif(field == 'overview'):
            result.overview = value
        else:
            self.db.commit()    
            return False
        self.db.commit()
        return True
