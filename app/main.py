from fastapi import FastAPI

from app.api.api_v1.api import api_router


description = """
E-commerce platform API to manage products.

## Products

You will be able to:

* **Show products**.
* **Create products**.
* **Update products**.
* **Delete products**.
"""

app = FastAPI(
    title="E-commerce platform API",
    description=description,
    version="0.0.1",
    contact={
        "name": "Rami BELGACEM",
        "url": "https://github.com/ramibelgacem/product-ecommerce-api",
        "email": "ramibelgacem@gmail.com",
    },
)

app.include_router(api_router, prefix="/api/v1")
