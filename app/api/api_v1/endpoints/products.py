import os

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse

from app import schemas
from app.exception import ProductNotFound
from app.db.orm import HtmlTableORM


base = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
db_file = os.path.join(base, "templates/index.html")
db = HtmlTableORM(db_file)

router = APIRouter()


@router.get("/")
def display_products():
    return FileResponse(db_file)


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_product(product: schemas.Product):
    db.add(product)
    return product


@router.put(
    "/{product_id}",
    status_code=status.HTTP_202_ACCEPTED,
)
def update_product(product_id: int, product: schemas.Product):
    try:
        db.update(product_id, product)
    except ProductNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id={product_id} does not exist",
        )
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_product(product_id: int):
    try:
        db.remove(product_id)
    except ProductNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id={product_id} does not exist",
        )
