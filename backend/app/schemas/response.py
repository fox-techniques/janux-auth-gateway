from pydantic import BaseModel


class ConflictResponse(BaseModel):
    detail: str
