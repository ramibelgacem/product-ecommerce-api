from pydantic import BaseModel, Field


class Product(BaseModel):
    name: str
    description: str | None = None
    price: float = Field(gt=0, description="The price must be greater than zero")


class ProductIn(Product):
    id: int
