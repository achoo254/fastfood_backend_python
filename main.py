import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

import settings
from api.crud.account import accountRouter
from api.crud.category import categoryRouter
from api.crud.order import orderRouter

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8017",
    "http://103.75.184.109",
    "https://103.75.184.109",
    "http://fastfood.hoandat.tech",
    "https://fastfood.hoandat.tech",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(accountRouter)
app.include_router(categoryRouter)
app.include_router(orderRouter)

if __name__ == "__main__":
    uvicorn.run(app,
                host=settings.HOST,
                port=settings.PORT)
