from bs4 import BeautifulSoup

from exception import ProductNotFound


class HtmlORM:
    def __init__(self, filename):
        self.filename = filename

    def get_content(self):
        html = open(self.filename)
        return BeautifulSoup(html, "html.parser")

    def _commit(self, soup):
        with open(self.filename, "wb") as f_output:
            f_output.write(soup.prettify("utf-8"))

    def add(self, product):
        html = open(self.filename)
        soup = BeautifulSoup(html, "html.parser")

        table = soup.find("table", {"id": "productsInfo"})
        table.append(
            BeautifulSoup(
                f"<tr id='{product.id}'><td>{product.id}</td><td>{product.name}</td>"
                f"<td>{product.description}</td><td>{product.price}</td></tr>",
                "html.parser",
            )
        )

        with open(self.filename, "wb") as f_output:
            f_output.write(soup.prettify("utf-8"))

    def remove(self, product_id):
        soup = self.get_content()

        product_tag = soup.find("tr", {"id": product_id})
        if product_tag is None:
            raise ProductNotFound()
        product_tag.decompose()

        self._commit(soup)
