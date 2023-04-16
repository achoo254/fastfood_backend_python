from api.models.account import Account


def response(data) -> dict:
    return {
        "data": data
    }


def account_response(data) -> dict:
    return {
        "id": str(data["_id"]) if "_id" in data else "",
        "username": data["username"] if "username" in data else "",
        "fullname": data["fullname"] if "fullname" in data else "",
        "role": data["role"] if "role" in data else "",
        "created": data["created"] if "created" in data else "",
        "token": data["token"] if "token" in data else "",
    }


def category_response(data) -> dict:
    return {
        "id": str(data["_id"]) if "_id" in data else "",
        "name": data["name"] if "name" in data else "",
        "products": data["products"] if "products" in data else [],
    }


def order_response(data) -> dict:
    return {
        "id": str(data["_id"]) if "_id" in data else "",
        "account": data["account"] if "account" in data else None,
        "table": data["table"] if "table" in data else 0,
        "count_person": data["count_person"] if "count_person" in data else 0,
        "products": data["products"] if "products" in data else [],
        "status": data["status"] if "status" in data else "",
        "final_amount": data["final_amount"] if "final_amount" in data else 0,
        "created": data["created"] if "created" in data else "",
    }
