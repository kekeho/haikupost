from pydantic import BaseModel
from datetime import datetime


class HaikuPost(BaseModel):
    haiku: str
    password: str


class Haiku(BaseModel):
    id: int
    content: str
    created_at: datetime
