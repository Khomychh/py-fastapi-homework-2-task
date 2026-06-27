import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict

from database.models import MovieStatusEnum


class Genre(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class Actor(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class Country(BaseModel):
    id: int
    code: str
    name: str | None = None

    model_config = ConfigDict(from_attributes=True)


class Language(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class MovieBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    date: datetime.date
    score: float
    overview: str
    status: MovieStatusEnum
    budget: Decimal = Field(ge=0, max_digits=15, decimal_places=2)
    revenue: float= Field(ge=0)


class MovieCreate(MovieBase):
    country_id: int
    genre_ids: list[int] = []
    actor_ids: list[int] = []
    language_ids: list[int] = []


class MovieUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=255)
    date: datetime.date | None = None
    score: float | None = None
    overview: str | None = None
    status: MovieStatusEnum | None = None
    budget: Decimal | None = Field(default=None, ge=0, max_digits=15, decimal_places=2)
    revenue: float | None = Field(default=None, ge=0)
    country_id: int | None = None
    genre_ids: list[int] | None = None
    actor_ids: list[int] | None = None
    language_ids: list[int] | None = None


class MovieListItemSchema(BaseModel):
    id: int
    name: str
    date: datetime.date
    score: float
    overview: str

    model_config = ConfigDict(from_attributes=True)


class MovieListResponseSchema(BaseModel):
    movies: list[MovieListItemSchema]
    prev_page: str | None
    next_page: str | None
    total_pages: int
    total_items: int


class MovieDetailSchema(MovieBase):
    id: int
    country: Country
    genres: list[Genre] = []
    actors: list[Actor] = []
    languages: list[Language] = []

    model_config = ConfigDict(from_attributes=True)
