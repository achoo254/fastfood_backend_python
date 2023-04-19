from dataclasses import dataclass
from typing import Optional, TypeVar, Any, Type, cast

from pydantic import BaseModel, Field

T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()
@dataclass
class Product:
    name: str
    image: str
    price: int
    note: str
    count: int

    @staticmethod
    def from_dict(obj: Any) -> 'Product':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        image = from_str(obj.get("image"))
        price = from_int(obj.get("price"))
        note = from_str(obj.get("note"))
        count = from_int(obj.get("count"))
        return Product(name, image, price, note, count)

    def to_dict(self) -> dict:
        result: dict = {"name": from_str(self.name), "image": from_str(self.image), "price": from_int(self.price),
                        "note": from_str(self.note), "count": from_int(self.count)}
        return result


def product_from_dict(s: Any) -> Product:
    return Product.from_dict(s)


def product_to_dict(x: Product) -> Any:
    return to_class(Product, x)


class Category(BaseModel):
    _id: Optional[str] = Field(alias="_id")
    name: Optional[str]
    products: list = []
