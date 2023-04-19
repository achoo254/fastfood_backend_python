from bson import ObjectId
from fastapi import APIRouter, HTTPException, Depends

from api.crud.account import get_current_user
from api.models.category import Category, Product
from api.utils.database import db
from api.utils.utils import convert_products_to_models
from body_response import response, category_response

categoryRouter = APIRouter()


@categoryRouter.post("/category/create")
async def create_category(data: Category, current_user: dict = Depends(get_current_user)):
    try:
        # kiểm tra có phải admin ko
        if current_user['role'] != 'Quản lý':
            raise HTTPException(status_code=500, detail='Không có quyền truy cập')
        # kiểm tra đã tồn tại chưa
        category = db.category.find_one({'name': data.name})
        if category:
            raise HTTPException(status_code=500, detail='tên đã tồn tại')
        else:
            data.products = convert_products_to_models(data)
            # convert to dict
            document = data.dict()
            # add db
            result = db.category.insert_one(document)
            # return
            return response(category_response({"_id": result.inserted_id}))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e.__dict__.get('detail') if e.__dict__.get('detail') else e))
@categoryRouter.put("/category/{category_id}")
async def update_category(category_id: str, data: Category, current_user: dict = Depends(get_current_user)):
    try:
        # kiểm tra có phải admin ko
        if current_user['role'] != 'Quản lý':
            raise HTTPException(status_code=500, detail='Không có quyền truy cập')
        else:
            # update
            data.products = convert_products_to_models(data)
            result = db.category.replace_one({"_id": ObjectId(category_id)}, data.dict())
            return response(category_response({"_id": result.modified_count}))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e.__dict__.get('detail') if e.__dict__.get('detail') else e))

@categoryRouter.delete("/category/{category_id}")
async def delete_category(category_id: str, current_user: dict = Depends(get_current_user)):
    try:
        # kiểm tra có phải admin ko
        if current_user['role'] != 'Quản lý':
            raise HTTPException(status_code=500, detail='Không có quyền truy cập')
        else:
            result = db.category.delete_one({"_id": ObjectId(category_id)})
            if result.deleted_count == 1:
                return response(category_response({"_id": result.deleted_count}))
            else:
                raise HTTPException(status_code=500, detail="Không tìm thấy danh mục")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e.__dict__.get('detail') if e.__dict__.get('detail') else e))


@categoryRouter.get("/category")
async def get_categories(current_user: dict = Depends(get_current_user)):
    try:
        categories = []
        for cate in db.category.find():
            categories.append(category_response(cate))
        return response(categories)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@categoryRouter.get("/category/{category_id}")
async def get_category(category_id: str, current_user: dict = Depends(get_current_user)):
    try:
        # kiểm tra có phải admin ko
        if current_user['role'] != 'Quản lý':
            raise HTTPException(status_code=500, detail='Không có quyền truy cập')
        else:
            category = db.category.find_one({"_id": ObjectId(category_id)})
            if category:
                # return
                return response(category_response(category))
            else:
                raise HTTPException(status_code=500, detail='Không tìm thấy kết quả')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e.__dict__.get('detail') if e.__dict__.get('detail') else e))
