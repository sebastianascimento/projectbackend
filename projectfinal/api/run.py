import uvicorn
from api import main


if __name__ == "__main__":
    uvicorn.run(
        app=main.api,
        host="0.0.0.0",
        reload=True
    )