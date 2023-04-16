import os

from fastapi import status
from fastapi.testclient import TestClient

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


def test_read_products():
    response = client.get("/api/v1/products/")

    assert response.status_code == status.HTTP_200_OK


def test_add_product():
    response = client.post(
        "/api/v1/products/",
        json={"id": 1, "name": "PC", "description": "PC gamer", "price": 1599},
    )
    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "name": "PC",
        "description": "PC gamer",
        "price": 1599,
    }


def test_update_product():
    response = client.put(
        "/api/v1/products/1",
        json={
            "id": 1,
            "name": "Personal Computer",
            "description": "PC gamer",
            "price": 1599,
        },
    )

    assert response.status_code == status.HTTP_202_ACCEPTED
    response = response.json()
    assert response["name"] == "Personal Computer"


def test_update_inexistant_product():
    product_id = 23
    response = client.put(
        f"/api/v1/products/{product_id}",
        json={
            "id": 23,
            "name": "Tablet",
            "price": 145.99,
        },
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == f"Product with id={product_id} does not exist"


def test_remove_product():
    response = client.delete("/api/v1/products/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_remove_inexistant_product():
    product_id = 23
    response = client.delete(f"/api/v1/products/{product_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == f"Product with id={product_id} does not exist"
