import json
from typing import List, Optional
from fastapi import HTTPException, status
from api.models import Movies
import logging

logging.basicConfig(filename='app.log', level=logging.DEBUG)


def load_movies_data(db: str) -> List[dict]:
    try:
        with open(db, "r") as data:
            result = json.loads("".join(data.readlines()))
        return result
    except FileNotFoundError as e:
        logging.error(f"Error: Movies data file not found: {db}")
        return []
    except json.JSONDecodeError as e:
        logging.error(f"Error: Invalid JSON format in movies data file: {e}")
        return []


def get_all_movies() -> List[dict] | None:
    try:
        movies_data = load_movies_data("/app/db.json")
        if not movies_data:
            return None

        filtered_data = [item for item in movies_data if isinstance(item, dict)]

        if not filtered_data:
            return None

        return filtered_data

    except Exception as e:
        logging.error(f"Error loading movies data: {e}")
        return None


def convert_to_dict(item) -> dict:
    return item


def get_movie_by_id(movie_id: str) -> Optional[Movies]:
    try:
        assert type(movie_id) is str
        assert movie_id

        movies: List[dict] = load_movies_data("/app/db.json")

        result = list(filter(lambda p: p['id'] == movie_id, movies))

        result = result.pop(0) if result else None

        return Movies(**result) if type(result) is dict else None

    except Exception as e:
        logging.error(f"Error retrieving movie item by ID: {e}")
        return None


def get_movie_by_title(movie_title: str) -> Optional[Movies]:
    try:
        assert isinstance(movie_title, str) and movie_title.strip(), "Invalid movie title"

        movies_data = load_movies_data("/app/db.json")
        if not movies_data:
            return None

        for movie in movies_data:
            if movie.get('title') == movie_title:
                return Movies(**movie)

        return None

    except Exception as e:
        logging.error(f"Error retrieving movie item by title: {e}")
        return None


def get_movies_by_category(category: str) -> List[dict] | None:
    try:
        assert isinstance(category, str) and category.strip(), "Invalid category"

        movies_data = load_movies_data("/app/db.json")
        if not movies_data:
            return None

        filtered_movies = [movie for movie in movies_data if movie.get('category') == category]

        if not filtered_movies:
            return None

        return filtered_movies

    except Exception as e:
        logging.error(f"Error loading movies data by category '{category}': {e}")
        return None


def post_create_movie(movie_id: str, data: Optional[dict] = None) -> Optional[Movies]:
    try:
        assert isinstance(movie_id, str), "movie_id must be a string"
        if not data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing data in request body")

        movies: List[dict] = load_movies_data("/app/db.json")

        if any(item['id'] == movie_id for item in movies):
            logging.error(f"Movie item with ID '{movie_id}' already exists.")
            return None

        data['id'] = movie_id
        movies.append(data)

        try:
            with open("/app/db.json", "w") as file:
                json.dump(movies, file, indent=4)
        except Exception as e:
            logging.error(f"Error saving movie item to database: {e}")
            return None

        return Movies(**data)

    except Exception as e:
        logging.error(f"An error occurred while creating movie item: {e}")
        return None


def save_movies_data(db: str, data: List[dict]) -> None:
    try:
        with open(db, "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        logging.error(f"Error saving data to database: {e}")


def delete_movie_by_id(movie_id: str) -> None:
    assert isinstance(movie_id, str), "movie_id must be a string"

    movies_data = load_movies_data("/app/db.json")
    filtered_movies = [item for item in movies_data if item['id'] != movie_id]

    if len(filtered_movies) == len(movies_data):
        logging.error(f"Error: Movie item with ID '{movie_id}' not found.")
        return

    save_movies_data("/app/db.json", filtered_movies)
    logging.info(f"Movie item with ID '{movie_id}' has been deleted.")


def update_movie(movie_id: str, data: dict) -> Optional[Movies]:
    try:
        assert isinstance(movie_id, str), "movie_id must be a string"
        if not data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing data in request body")

        movies_data = load_movies_data("/app/db.json")
        movie_index = None

        for index, movie in enumerate(movies_data):
            if movie['id'] == movie_id:
                movie_index = index
                break

        if movie_index is None:
            logging.error(f"Movie item with ID '{movie_id}' not found.")
            return None

        updated_movie = {**movies_data[movie_index], **data}
        movies_data[movie_index] = updated_movie

        try:
            with open("/app/db.json", "w") as file:
                json.dump(movies_data, file, indent=4)
        except Exception as e:
            logging.error(f"Error saving updated movie item to database: {e}")
            return None

        return Movies(**updated_movie)

    except Exception as e:
        logging.error(f"An error occurred while updating movie item: {e}")
        return None
