from typing import Optional

from pydantic import BaseModel, Field
from pydantic.schema import datetime



class Order(BaseModel):
    _id: Optional[str] = Field(alias="_id")
    account: Optional[object]
    table: Optional[str]
    count_person: Optional[int]
    products: list = []
    status: Optional[str]
    total_amount: Optional[int]
    final_amount: Optional[int]
    created: datetime = Field(default_factory=datetime.now)
