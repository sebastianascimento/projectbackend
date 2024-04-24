from fastapi import FastAPI
from api.routes import (
    movies
)

api = FastAPI(
    title= "Movie Api",
    description= "This API provides movies data to our website,"
)

routers =[
    movies.router
]

for router in routers:
    api.include_router(router=router)

    