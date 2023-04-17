from bs4 import BeautifulSoup

from app import schemas
from app.exception import ProductNotFound


class HtmlTableInterface:
    """
    It is a class that serves as an interface between the application program
    and the html file that acts as a database.
    """

    def __init__(self, filename: str):
        """initialise a new database interface with html file path

        :param filename: database html file
        :type filename: str
        """
        self.filename = filename

    def get_content(self):
        """Get the content of the database html file
        using BeautifulSoup library

        :return: database html file content
        :rtype: BeautifulSoup
        """
        html = open(self.filename)
        return BeautifulSoup(html, "html.parser")

    def _commit(self, soup: BeautifulSoup):
        """Validate new changement in the database html file

        :param soup: beautifulSoup object that holds the new changement
        :type soup: BeautifulSoup
        """
        with open(self.filename, "wb") as f_output:
            f_output.write(soup.prettify("utf-8"))

    def add(self, product: schemas.ProductIn):
        """Create a new product

        :param product: product object holds informations
        :type product: ProductIn
        """
        soup = self.get_content()

        table = soup.find("table", {"id": "productsInfo"})
        table.append(
            BeautifulSoup(
                f"<tr id='{product.id}'><td id='id'>{product.id}</td><td id='name'>{product.name}</td>"
                f"<td id='description'>{product.description}</td><td id='price'>{product.price}</td></tr>",
                "html.parser",
            )
        )

        self._commit(soup)

    def update(self, product_id: int, product: schemas.Product):
        """Update a product

        :param product_id: id of the product to be updated
        :type product_id: int
        :param product: product object holds informations to update
        :type product: schemas.Product
        :raises ProductNotFound: if the product does not exist
        """
        if not isinstance(product, dict):
            product = dict(product)

        soup = self.get_content()

        product_tag = soup.find("tr", {"id": product_id})
        if product_tag is None:
            raise ProductNotFound()

        for key in product.keys():
            product_tag.find("td", {"id": key}).string.replace_with(str(product[key]))

        self._commit(soup)

    def remove(self, product_id: int):
        """Delete a product

        :param product_id: id of the product to be deleted
        :type product_id: int
        :raises ProductNotFound: if the product does not exist
        """
        soup = self.get_content()

        product_tag = soup.find("tr", {"id": product_id})
        if product_tag is None:
            raise ProductNotFound()
        product_tag.decompose()

        self._commit(soup)

    def clear(self):
        """Remove all product from the database html files"""
        soup = self.get_content()

        lines = soup.findAll("tr", id=True)
        for line in lines:
            line.decompose()

        self._commit(soup)
