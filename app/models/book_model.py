from pydantic import BaseModel, Field
from typing import Optional

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, description="Title of the book")
    author: Optional[str] = Field(None, description="Author of the book")
    description: Optional[str] = Field(None, description="Description of the book")
    available_copies: Optional[int] = Field(None, ge=0, description="Number of available copies")
