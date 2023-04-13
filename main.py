from fastapi import FastAPI
from pydantic import BaseModel


class Product(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float


app = FastAPI()


@app.post("/products/")
def create_product(product: Product):
    return product
