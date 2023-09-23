import os

import redis as r

from fastapi import FastAPI

from pydantic import BaseModel, Field
from typing import List, Dict


app = FastAPI()

REDIS = os.environ.get('REDIS', 'redis://localhost:6379')

redis = r.Redis.from_url(REDIS)


@app.get("/")
async def root():
    return {"message": "Hello World"}


class Order(BaseModel):
    id: int
    item: str
    quantity: int
    price: float = Field(..., ge=0)
    status: str


class Orders(BaseModel):
    orders: List[Order]
    criterion: str


@app.post("/solution")
async def process_orders(orders: Orders) -> Dict[str, float]:
    orders_json = orders.model_dump_json()

    if (result := redis.get(orders_json)) is not None:
        total_revenue = result
    else:
        total_revenue = 0
        for order in orders.orders:
            if orders.criterion == 'all' or order.status == orders.criterion:
                total_revenue += order.quantity * order.price
        redis.set(orders_json, total_revenue)
    return {"total_revenue": total_revenue}
