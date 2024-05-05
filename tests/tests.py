from api.db import get_movies
from api.models import Movie


# The function executes a database query to retrieve all movies.
def test_returns_all_movies(self):
    # Arrange
    expected_movies = [
        Movie(id=1, title="Movie 1", year="2021", description="Description 1", rating=4.5, ranking=1, review="Review 1", img_url="img1.jpg"),
        Movie(id=2, title="Movie 2", year="2022", description="Description 2", rating=4.0, ranking=2, review="Review 2", img_url="img2.jpg"),
        Movie(id=3, title="Movie 3", year="2023", description="Description 3", rating=3.5, ranking=3, review="Review 3", img_url="img3.jpg")
    ]

    # Act
    actual_movies = get_movies()

    # Assert
    assert actual_movies == expected_movies