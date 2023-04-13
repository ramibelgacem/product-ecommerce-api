from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel


class Product(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float


app = FastAPI()


@app.get("/")
def display_products():
    return FileResponse("index.html")


@app.post("/products/")
def create_product(product: Product):
    return product
