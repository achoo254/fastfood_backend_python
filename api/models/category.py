from typing import Optional

from pydantic import BaseModel, Field


class Product:
    name: str
    image: str
    price: int
    note: str


class Category(BaseModel):
    _id: Optional[str] = Field(alias="_id")
    name: Optional[str]
    products: list = []
