from fastapi import APIRouter

from app.api.api_v1.endpoints import products

api_router = APIRouter()
api_router.include_router(products.router, prefix="/products", tags=["Products"])
