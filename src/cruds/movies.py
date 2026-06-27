from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import MovieModel

async def get_movies(db: AsyncSession, offset: int = 0, limit: int = 10):
    stmt = select(MovieModel).offset(offset).limit(limit).order_by(MovieModel.id)
    result = await db.execute(stmt)
    movies = result.scalars().all()
    return movies