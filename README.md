# E-commerce platform API!

## Requirements
- python 3.10+
- pip3

## Setup
- Create a new directory, e.g product_ecommerce_api and move into it
- Create a new python environment
```
python3 -m venv venv
```
- Activate it
```
source venv/bin/activate
```
- Clone this repository and navigate into it
- Install requirements
```
pip3 install -r requirements.txt
```
- Run uvicorn server
```
uvicorn app.main:app --reload
```

## How to use it
Open the navigator and access to this URL: http://0.0.0.0:8000/docs, you will find all the APIs available

## Test
To run the tests, you need to install dev requirements
```
pip3 install -r requirements-dev.txt
```
and run the pytest command with coverage functionnality
```
pytest --cov --cov-report=html:htmlcov --cov-config=.coveragerc
```

## API
**Products**
- GET --> /api/v1/products: Read html file content
- POST --> /api/v1/products: Create a new product
- PUT --> /api/v1/products/{user_id}: Update a product
- DELETE --> /api/v1/products/{user_id}: Remove a product

## Roadmap
Things that can be added or improved
- Product ID: implement a system to check if a new product ID already exists or to automatically generate a new one.
- /sort endpoint:  sort products in the html page based on its price
- Settings: the ability to choose the database html file in a configuration file
- Logging: log operations in the HtmlTableInterface class
- Linting and formatting: Add pre-commit
