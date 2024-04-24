from pydantic import BaseModel
from typing import Optional

class Movies(BaseModel):
    id: str
    title: str
    category: str
    launch: Optional[str]
    stream: Optional[str] 

    