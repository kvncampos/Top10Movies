from typing import Dict, List
from sqlmodel import SQLModel, create_engine, Session, select, update
from .models import Movie
from icecream import ic

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///instance/{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def db_get_movies() -> list:
    """
    The function executes a database query to retrieve all movies.

    Returns:
        list: A list of all movies.
    """
    with Session(engine) as session:
        # Retrieve the top 10 movies ordered by rating
        statement = select(Movie).order_by(Movie.rating.desc()).limit(10)
        results = session.exec(statement).all()

        # Update the ranking for each movie
        _db_update_ranking(session, results)

        # Retrieve the updated list of movies with their rankings
        updated_results = session.exec(statement).all()

    return updated_results

def db_get_movie(movie_data: dict):
    """
    Retrieve the top 10 movies based on their rating and update their rankings.

    Returns:
        List[Movie]: A list of Movie objects representing the top 10 movies.

    Raises:
        None

    Example Usage:
        movies = db_get_movie()
        for movie in movies:
            print(movie.original_title)
    """
    with Session(engine) as session:
        statement = select(Movie).where(Movie.original_title == movie_data['original_title'])
        result = session.exec(statement).first()
    return result
    
def _db_update_ranking(session: Session, movies: List[Movie]) -> None:
    for num, movie in enumerate(movies, start=1):
        # Check if the current ranking is already the desired value
        if movie.ranking != num:
            # Update the ranking for the current movie
            movie.ranking = num

            # Add the updated movie to the session
            session.add(movie)

    # Commit the transaction to persist the changes
    session.commit()
        

def db_add_movie(movie_data: dict) -> bool:
    """
    Add a movie to the database.

    Parameters:
    - Model_data: The data of the movie to be added. Should be an instance of the Movie model.

    Returns:
    None

    Example usage:
    movie = Movie(title="Inception", director="Christopher Nolan")
    add_movie(movie)
    """
    with Session(engine) as session:
            try:
                stmt = select(Movie).where(Movie.original_title == movie_data['original_title'])
                existing_movie = session.exec(stmt).first()
                if existing_movie is None:
                    movie = Movie(**movie_data)
                    session.add(movie)
                    session.commit()
                    session.refresh(movie)
                    return True
                else:
                    return False
            except Exception as e:
                session.rollback()
                raise ValueError(f"Failed to add movie: {e}")

def db_update_movie(movie_id, new_rating, new_review) -> None:
    """
    Update the rating and review of a movie.

    Parameters:
    - movie_id (int): The ID of the movie to update.
    - new_rating (float): The new rating for the movie.
    - new_review (str): The new review for the movie.

    Returns:
    None

    Example Usage:
    update_movie(1, 4.5, "Great movie!")
    """
    # Create an update statement
    stmt = update(Movie).where(Movie.id == movie_id).values(
        rating=new_rating,
        review=new_review
    )
    with Session(engine) as session:
        # Execute the update statement within the provided session
        session.exec(stmt)

        # Commit the transaction to persist the changes
        session.commit()

        
def db_delete_movie(movie_id) -> None:
    """
    Delete a movie from the database based on the given query filter.

    Parameters:
    - query_filter: The filter to select the movie(s) to be deleted.

    Returns:
    None

    Raises:
    - NoResultFound: If no movie is found based on the given query filter.

    Example:
    delete_movie(Movie.title == "Inception")

    This will delete the movie with the title "Inception" from the database.
    """
    with Session(engine) as session:
        statement = select(Movie).where(Movie.id == movie_id)
        results = session.exec(statement)
        movie = results.one()
        print("Movie: ", movie, "deleted from DB.")
        session.delete(movie)
        session.commit()
        