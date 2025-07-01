from typing import Optional

from pydantic import BaseModel


class EmployeeCreate(BaseModel):
    full_name: str
    email: str


class EmployeeOut(BaseModel):
    id: int
    full_name: str
    email: str
    photo_url: Optional[str] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
