from sqlmodel import select
from app.models import Movie, MovieCreate

class MovieService():
    
    def __init__(self, db) -> None:
        self.db = db

    async def get_movies(self):
        result = await self.db.execute(select(Movie))
        result = result.scalars().all()
        return result

    async def get_movie(self, id):
        movies = await self.db.execute(select(Movie).where(Movie.id==id))
        result = movies.scalars().first()
        return result

    async def get_movies_by_category(self, category):
        result = self.db.query(Movie).filter(Movie.category == category).all()
        return result

    async def create_movie(self, movie: Movie):
        # movie = Movie(title=movie.title, overview=movie.overview, year=movie.year, rating=movie.rating, category=movie.category)
        new_movie = Movie(**movie.dict())
        self.db.add(new_movie)
        await self.db.commit()
        await self.db.refresh(new_movie)
        return

    async def update_movie(self, id: int, data: MovieCreate):
        movie_old = await MovieService(self.db).get_movie(id)
        movie_old.title = data.title
        movie_old.overview = data.overview
        movie_old.year = data.year
        movie_old.rating = data.rating
        movie_old.category = data.category
        self.db.add(movie_old)
        await self.db.commit()
        return

    async def delete_movie(self, id: int):
        movie = await MovieService(self.db).get_movie(id)
        await self.db.delete(movie)
        await self.db.commit()
        return