import os

from fastapi import FastAPI, status
from fastapi.responses import FileResponse
from pydantic import BaseModel

from model import HtmlORM

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db = HtmlORM(os.path.join(base, "index.html"))


class Product(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float


app = FastAPI()


@app.get("/")
def display_products():
    return FileResponse(f"{base}/index.html")


@app.post("/products/", status_code=status.HTTP_201_CREATED)
def add_product(product: Product):
    db.add(product)
    return product
