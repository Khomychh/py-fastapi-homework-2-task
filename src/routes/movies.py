from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from cruds.movies import get_movies
from database import get_db, MovieModel
from database.models import CountryModel, GenreModel, ActorModel, LanguageModel
from schemas.movies import MovieListResponseSchema

router = APIRouter()

@router.get("/movies/", response_model=list[MovieListResponseSchema])
async def list_movies(
    page: Annotated[int, Query(ge=1)] = 1,
    per_page: Annotated[int, Query(ge=1, le=20)] = 10,
    db: AsyncSession = Depends(get_db)
):
    offset = (page - 1) * per_page
    movies = await get_movies(db, offset=offset, limit=per_page)

    if not movies:
        raise HTTPException(status_code=404, detail="Movies not found")

    count_items = await db.execute(select(func.count(MovieModel.id)))
    total_items = count_items.scalar_one()
    total_pages = (total_items + per_page - 1) // per_page

    prev_page = f"/theater/movies/?page={page - 1}&per_page={per_page}" if page > 1 else None
    next_page = f"/theater/movies/?page={page + 1}&per_page={per_page}" if page < total_pages else None

    return MovieListResponseSchema(
        movies=movies,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items
    )
