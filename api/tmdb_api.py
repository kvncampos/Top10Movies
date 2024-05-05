from os import environ
import requests
from icecream import ic
from pydantic import Field
from typing import Dict, Any, List
from pydantic.dataclasses import dataclass
from dotenv import load_dotenv
# from utils import basic_logging as log

load_dotenv()  # take environment variables from .env.


@dataclass
class TMDBApi:
    """
    TMDBApi class for interacting with the TMDB API.

    Attributes:
    - token (str): Uses Environment VAR "TMDB_API_READ_ONLY"

    Methods:
    - search_movie(query: str, include_adult: bool = False, language: str = "en-US", page: int = 1) -> dict:
        Search for movies in the TMDB API based on the given query.

        Parameters:
        - query (str): The search query.
        - include_adult (bool): Whether to include adult movies in the search results. Default is False.
        - language (str): The language for the search results. Default is "en-US".
        - page (int): The page number for the search results. Default is 1.

        Returns:
        - Dict: The search results in JSON format.
    """
    token: str = environ.get("TMDB_API_READ_ONLY")
    api_website: str = 'https://api.themoviedb.org'
    
    def __post_init__(self):
        if not self.token:
            raise ValueError("TMDB read token not provided. Set TMDB_READ_TOKEN environment variable.")
    
    @property
    def _headers(self) -> Dict:
        return {
            "accept": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
    
    def search_movie(self, query: str, include_adult: bool = False, language: str = "en-US", page: int = 1) -> List[Dict]:
        """
        TMDBApi class for interacting with the TMDB API.

        Attributes:
        - token (str): The TMDB read token.
        - _MOVIE_SEARCH_ENDPOINT (str): The endpoint for searching movies in the TMDB API.

        Methods:
        - search_movie(query: str, include_adult: bool = False, language: str = "en-US", page: int = 1) -> dict:
            Search for movies in the TMDB API based on the given query.

            Parameters:
            - query (str): The search query.
            - include_adult (bool): Whether to include adult movies in the search results. Default is False.
            - language (str): The language for the search results. Default is "en-US".
            - page (int): The page number for the search results. Default is 1.

            Returns:
            - Dict: The search results in JSON format.

        """
        MOVIE_SEARCH_ENDPOINT: str = f'{self.api_website}/3/search/movie'
        params = {
            "query": query,
            "include_adult": str(include_adult).lower(),
            "language": language,
            "page": page
        }
        response = requests.get(
            url=MOVIE_SEARCH_ENDPOINT, headers=self._headers, params=params
            ).json()
        
        # Sort the movie results based on popularity in descending order
        sorted_popularity = sorted(response['results'], key=lambda x: x['popularity'], reverse=True)

        # Select the top 5 movies with the highest popularity
        top_10_movies = sorted_popularity[:10]
        
        # List Comprension to Find Relevant Data
        keys_to_find = ['original_title', 'id', 'vote_count', 'release_date', 'overview']
        movie_list = [{k: v for k, v in movie.items() if k in keys_to_find} for movie in top_10_movies]

        # Sort the movie results based on Latest Year in descending order
        sorted_release_date = sorted(movie_list, key=lambda x: x['release_date'], reverse=True)
        
        return sorted_release_date
    
    def movie_details(self, movie_id: int, language: str = "en-US") -> Dict:
        """
        Get the details of a movie from the TMDB API.

        Parameters:
        - movie_id (int): The ID of the movie.
        - language (str): The language for the movie details. Default is "en-US".

        Returns:
        - dict: The movie details including the original title, poster path, release date, and overview.
        """
        MOVIE_DETAILS_ENDPOINT = f'{self.api_website}/3/movie/{movie_id}?{language}'
        MOVIE_IMAGE_BASE = 'https://image.tmdb.org/t/p/original/'
        
        response = requests.get(MOVIE_DETAILS_ENDPOINT, headers=self._headers).json()
        
        # Keys To Look For
        keys_to_find = ['original_title', 'poster_path', 'release_date', 'overview']
        # Dict Comprehension to Get Relevant Key/Value Data
        movie_data = {k: v if k != 'poster_path' else MOVIE_IMAGE_BASE + v for k, v in response.items() if k in keys_to_find}
        
        return movie_data
        

if __name__ == '__main__':
    
    movie_api = TMDBApi()
    
    result = movie_api.search_movie("Oceans Eleven")
    # ic(result)
    # log.debug("This was ran, locally and not imported.")