from bson import ObjectId
from fastapi import APIRouter, HTTPException, Depends

from api.crud.account import get_current_user
from api.models.order import Order
from api.utils.database import db
from body_response import order_response, response

orderRouter = APIRouter()


@orderRouter.post("/order/create")
async def create_order(data: Order, current_user: dict = Depends(get_current_user)):
    try:
        # convert to dict
        document = data.dict()
        # add db
        result = db.order.insert_one(document)
        # init value return
        data_response = db.order.find_one({"_id": ObjectId(result.inserted_id)})
        # return
        return response(order_response(data_response))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@orderRouter.post("/order/{order_id}")
async def update_order(order_id: str, data: Order, current_user: dict = Depends(get_current_user)):
    try:
        result = db.order.replace_one({"_id": ObjectId(order_id)}, data.dict())
        return response(order_response({"_id": result.modified_count}))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@orderRouter.get("/order")
async def get_orders(current_user: dict = Depends(get_current_user)):
    try:
        orders = []
        for order in db.order.find():
            orders.append(order_response(order))
        return response(orders)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
