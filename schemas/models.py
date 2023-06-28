from pydantic import Field, BaseModel
from typing import Optional
import datetime

class Movie(BaseModel):

    id: Optional[int] = None
    title:str = Field(min_length=1, max_length=30)
    overview:str = Field(max_length=100, min_length=1)
    year:int = Field(ge=datetime.date.today().year)
    rating:float = Field(ge=0, le=10)
    category:str = Field(min_length=1,max_length=30)

    class Config:
        schema_extra = {
            "example" : {
                "title" : "Movie",
                "overview" : "Movie Overview",
                "year" : datetime.date.today().year,
                "rating" : 10,
                "category" : "Movie category"
            }
        }


class User(BaseModel):

    email:str = Field(min_length=3)
    password:str = Field(min_length=1)

    class Config:
          schema_extra = {
            "example" : {
                "email" : "admin@gmail.com",
                "password" : "admin",
            }
        }
    