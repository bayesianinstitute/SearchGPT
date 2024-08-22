from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str
    history: list = None
