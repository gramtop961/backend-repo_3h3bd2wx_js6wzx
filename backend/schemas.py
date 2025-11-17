from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

# Each model corresponds to a Mongo collection with its lowercase name

class Subscriber(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    company: Optional[str] = None
    source: Optional[str] = Field(default="website")

class Lead(BaseModel):
    name: str
    email: EmailStr
    company: Optional[str] = None
    message: Optional[str] = None
    plan: Optional[str] = Field(default="free")

class Testimonial(BaseModel):
    author: str
    role: Optional[str] = None
    content: str
    rating: Optional[int] = Field(default=5, ge=1, le=5)

# Common response model for health/test
class HealthResponse(BaseModel):
    backend: str
    database: str
    database_url: str
    database_name: str
    connection_status: str
    collections: list[str] = []
    timestamp: datetime
