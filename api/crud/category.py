from fastapi import APIRouter, HTTPException, Depends

from api.crud.account import get_current_user
from api.models.category import Category
from api.utils.database import db
from body_response import response, category_response

categoryRouter = APIRouter()


@categoryRouter.post("/category/create")
async def create_category(data: Category, current_user: dict = Depends(get_current_user)):
    # kiểm tra đã tồn tại chưa
    category = db.category.find_one({'name': data.name})
    if category:
        raise HTTPException(status_code=500, detail='name đã tồn tại')
    else:
        # convert to dict
        document = data.dict()
        # add db
        result = db.category.insert_one(document)
        # return
        return response(category_response({"_id": result.inserted_id}))


@categoryRouter.get("/category")
async def get_categories(current_user: dict = Depends(get_current_user)):
    try:
        categories = []
        for cate in db.category.find():
            categories.append(category_response(cate))
        return response(categories)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
