from typing import List
from fastapi import APIRouter, HTTPException, status
from api.clients import get_movie_by_id, get_all_movies , get_movie_by_title , post_create_movie  , delete_movie_by_id , get_movies_by_category , update_movie
from api.models import Movies
import logging


logger = logging.getLogger(__name__)

router= APIRouter(prefix="/movie", tags=["Movie"])

@router.get("")
def get_all_movies_route() ->List [Movies]:
    try:
        movies_data = get_all_movies()

        if movies_data is None:
            return []  

        converted_data = [convert_to_dict(item) for item in movies_data]
        result = [Movies(**item) for item in converted_data]
        return result

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)




def convert_to_dict(data):
    return {
        'id': data['id'],
        'title': data['title'], 
        'category': data['category'],
        'launch': data['launch'],
        'stream': data['stream']
    }



@router.get("/{movie_id:str}")
def get_movie(movie_id: str) -> Movies | None:
    try:
        result: Movies | None = get_movie_by_id(movie_id=movie_id)

        if not result:
            logger.info(f"Movies item with ID '{movie_id}' not found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        assert type(result) is Movies
        logger.info(f"Movies item with ID '{movie_id}' found")
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")


@router.get("/title/{movie_title:str}")
def get_movie_by_title_route(movie_title: str) -> Movies:  
    try:
        result: Movies | None = get_movie_by_title(movie_title=movie_title) 
        if not result:
            logger.info(f"Movies item with title '{movie_title}' not found") 
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with title '{movie_title}' not found")

        assert type(result) is Movies
        logger.info(f"Movies item with title '{movie_title}' found")
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")


@router.get("/category/{movie_category:str}")
def get_movies_by_category_route(movie_category: str) -> List[dict]:
    try:
        movies_data = get_movies_by_category(movie_category)

        if movies_data is None:
            return []

        return movies_data

    except Exception as e:
        logging.error(f"Error retrieving movies by category '{movie_category}': {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
@router.post("/{movie_id:str}")
def create_movie(movie_id:str , data: dict) -> Movies:
    try:
        result: Movies | None = get_movie_by_id(movie_id=movie_id)

        if result:
            logger.info(f"News item with ID '{movie_id}' already exists")
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="News item with ID already exists")

        movie_movies = post_create_movie(movie_id=movie_id, data=data)
        if movie_movies:
            logger.info(f"New news item with ID '{movie_id}' has been created")
            return movie_movies
        else:
            logger.error(f"Failed to create new news item with ID '{movie_id}'")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create new news item")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")


@router.delete("/{movie_id}", response_model=dict)
def delete_movies(movie_id: str):
    assert isinstance(movie_id, str), "new_id must be a string"

    
    try:
        delete_movie_by_id(movie_id)
        logger.info(f"News item with ID '{movie_id}' has been deleted")
        return {"message": f"News item with ID '{movie_id}' has been deleted"}
    except Exception as e:
        logger.error(f"Error deleting news item with ID '{movie_id}': {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    



@router.put("/{movie_id:str}")
def update_movie_route(movie_id: str, data: dict) -> Movies:
    try:
        updated_movie = update_movie(movie_id=movie_id, data=data)

        if not updated_movie:
            logger.error(f"Failed to update movie item with ID '{movie_id}'")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie item with ID '{movie_id}' not found")

        logger.info(f"Movie item with ID '{movie_id}' has been updated")
        return updated_movie

    except HTTPException as he:
        raise he

    except Exception as e:
        logger.error(f"An unexpected error occurred while updating movie item with ID '{movie_id}': {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")
