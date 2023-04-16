from typing import Optional

from pydantic import BaseModel, Field
from datetime import datetime


class Account(BaseModel):
    _id: Optional[str] = Field(alias="_id")
    created: datetime = Field(default_factory=datetime.now)
    username: Optional[str]
    password: Optional[str]
    fullname: Optional[str]
    role: Optional[str]
    token: Optional[str]

