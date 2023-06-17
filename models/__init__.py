from dataclasses import dataclass, field
from pydantic import Field, BaseModel
from typing import Optional
import datetime

@dataclass
class Movie():

    id: Optional[int] = field(default=0)
    title:str = field(default="Movie")
    overview:str = field(default="Movie Overview")
    year:str = field(default=str(datetime.date.today().year))
    rating:float = field(default=10)
    category:str = field(default="Movie Category")

    def __init__(self, id:int, title:str,overview:str,year:str,rating:float,category:str):
        self.id =id
        self.title=title
        self.category=category
        self.year=year
        self.rating=rating
        self.overview=overview

