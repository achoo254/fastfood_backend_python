from typing import Optional

import bcrypt
import jwt as jwt
from bson import ObjectId
from fastapi import HTTPException, APIRouter, Header, Depends

from api.models.account import Account
from api.utils.database import db
from body_response import response, account_response

accountRouter = APIRouter()

# Mã khóa bí mật
secret_key = 'your_secret_key'


# Dependency function để đọc JWT token từ header
async def get_token(auth_header: Optional[str] = Header(None, alias="Token")):
    if auth_header is None:
        raise HTTPException(status_code=500, detail="Không tìm thấy JWT token trong header")

    # Kiểm tra xem JWT token có đúng định dạng hay không
    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        raise HTTPException(status_code=500, detail="JWT token không đúng định dạng")

    # Lấy JWT token
    token = parts[1]
    return token


# Hàm kiểm tra JWT token và trả về thông tin người dùng nếu hợp lệ
def get_user_info(token: str):
    try:
        # Giải mã JWT token bằng secret key
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        find_user = db.account.find_one({"_id": ObjectId(payload['id'])})
        if find_user:
            return payload
        else:
            raise HTTPException(status_code=500, detail="Tài khoản không tồn tại")
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=500, detail="JWT token không hợp lệ")


# Dependency function để đọc JWT token từ header và gọi hàm get_user_info
async def get_current_user(token: str = Depends(get_token)):
    return get_user_info(token)


@accountRouter.post("/account/create")
async def create_account(account: Account):
    # kiểm tra đã tồn tại chưa
    user = db.account.find_one({'username': account.username})
    if user:
        raise HTTPException(status_code=500, detail='username đã tồn tại')
    else:
        # encode password
        account.password = bcrypt.hashpw(account.password.encode('utf-8'), bcrypt.gensalt())
        # convert to dict
        document = account.dict()
        # add db
        result = db.account.insert_one(document)
        # create token
        token = jwt.encode({'id': str(result.inserted_id), 'username': account.username}, secret_key,
                           algorithm='HS256')
        # return
        return response(account_response({"token": token}))


@accountRouter.post("/account/login")
async def login(data: Account):
    # Get the user from MongoDB
    account = db.account.find_one({'username': data.username})
    if account:
        # Verify the password
        if bcrypt.checkpw(data.password.encode('utf-8'), account['password']):
            account['token'] = jwt.encode({'id': str(account['_id']), 'username': data.username}, secret_key,
                                          algorithm='HS256')
            return response(account_response(account))
        else:
            raise HTTPException(status_code=500, detail='password không chính xác!')
    else:
        raise HTTPException(status_code=500, detail='username không chính xác!')


@accountRouter.get("/accounts")
async def get_accounts(current_user: dict = Depends(get_current_user)):
    try:
        accounts = []
        for account in db.account.find():
            accounts.append(account_response(account))
        return response(accounts)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@accountRouter.get("/account")
async def get_account(current_user: dict = Depends(get_current_user)):
    account = db.account.find_one({"_id": ObjectId(current_user['id'])})
    if account:
        return response(account_response(account))
    else:
        raise HTTPException(status_code=500, detail="account không tồn tại")
