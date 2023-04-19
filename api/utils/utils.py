"""UTILS
Misc helpers/utils functions
"""

# # Native # #
from time import time
from uuid import uuid4
from typing import Union

__all__ = ("get_time", "get_uuid", "convert_products_to_models")

from api.models.category import Product


def get_time(seconds_precision=True) -> Union[int, float]:
    """Returns the current time as Unix/Epoch timestamp, seconds precision by default"""
    return time() if not seconds_precision else int(time())


def get_uuid() -> str:
    """Returns an unique UUID (UUID4)"""
    return str(uuid4())

def convert_products_to_models(data) -> list:
    new_update_product: list = []
    if data.products:
        for item in data.products:
            product = Product.from_dict(item)
            new_update_product.append(product.to_dict())
    return new_update_product
