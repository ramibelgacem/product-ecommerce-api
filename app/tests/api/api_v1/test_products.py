import os

from fastapi import status
from fastapi.testclient import TestClient

from app import schemas
from app.api.api_v1.endpoints.products import get_db
from app.db.htmltableinterface import HtmlTableInterface
from app.main import app


def override_get_db():
    base = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )
    db_file = os.path.join(base, "templates/test_index.html")
    db = HtmlTableInterface(db_file)
    return db


app.dependency_overrides[get_db] = override_get_db


client = TestClient(app)


def create_product(db, id, name, description, price):
    product = schemas.ProductIn(id=id, name=name, description=description, price=price)
    db.add(product)


def test_read_products():
    response = client.get("/api/v1/products/")

    assert response.status_code == status.HTTP_200_OK


def test_add_product():
    data = {"id": 1, "name": "PC", "description": "PC gamer", "price": 1599.65}
    response = client.post(
        "/api/v1/products/",
        json=data,
    )
    assert response.status_code == 201
    assert response.json() == data


def test_update_product(fake_db):
    product_id = 2
    create_product(fake_db, product_id, "Hard disk", "HDD hard disk", "54.5")
    data = {
        "name": "HDD",
        "price": 52,
    }
    response = client.put(
        f"/api/v1/products/{product_id}",
        json=data,
    )

    assert response.status_code == status.HTTP_202_ACCEPTED
    response = response.json()
    assert response["name"] == data["name"]
    assert response["price"] == data["price"]


def test_update_inexistant_product():
    data = {
        "name": "Tablet",
        "price": 145.99,
    }
    product_id = 3
    response = client.put(
        f"/api/v1/products/{product_id}",
        json=data,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == f"Product with id={product_id} does not exist"


def test_remove_product(fake_db):
    product_id = 4
    create_product(fake_db, product_id, "Hard disk", "HDD hard disk", "54.5")
    response = client.delete(f"/api/v1/products/{product_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_remove_inexistant_product():
    product_id = 5
    response = client.delete(f"/api/v1/products/{product_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == f"Product with id={product_id} does not exist"
