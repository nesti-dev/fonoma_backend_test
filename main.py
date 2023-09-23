from fastapi import FastAPI

from pydantic import BaseModel, Field
from typing import List

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


class Order(BaseModel):
    id: int
    item: str
    quantity: int
    price: float
    status: str


class Orders(BaseModel):
    orders: List[Order]
    criterion: str


@app.post("/solution")
async def process_orders(orders: Orders):
    total_revenue = 0
    for order in orders.orders:
        if orders.criterion == 'all' or order.status == orders.criterion:
            total_revenue += order.quantity * order.price
    return {"total_revenue": total_revenue}
