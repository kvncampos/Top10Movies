from typing import Optional
from sqlmodel import Field, SQLModel


class Movie(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    original_title: str = Field(unique=True)
    release_date: str
    overview: str
    rating: float | None = None
    ranking: int | None = None
    review: str | None = None
    poster_path: str
