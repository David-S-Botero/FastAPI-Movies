from dataclasses import dataclass

@dataclass
class Movie():
    id: int
    title:str
    overview:str
    year:str
    rating:float
    category:str

    def __init__(self, id:int, title:str,overview:str,year:str,rating:float,category:str):
        self.id =id
        self.title=title
        self.category=category
        self.year=year
        self.rating=rating
        self.overview=overview

    
