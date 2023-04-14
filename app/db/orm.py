from bs4 import BeautifulSoup

from exception import ProductNotFound


class HtmlTableORM:
    def __init__(self, filename):
        self.filename = filename

    def get_content(self):
        html = open(self.filename)
        return BeautifulSoup(html, "html.parser")

    def _commit(self, soup):
        with open(self.filename, "wb") as f_output:
            f_output.write(soup.prettify("utf-8"))

    def add(self, product):
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

    def update(self, product_id, product):
        if not isinstance(product, dict):
            product = dict(product)

        soup = self.get_content()

        product_tag = soup.find("tr", {"id": product_id})
        if product_tag is None:
            raise ProductNotFound()

        for key in product.keys():
            product_tag.find("td", {"id": key}).string.replace_with(str(product[key]))
            if "id" == key:
                product_tag[key] = product[key]

        self._commit(soup)

    def remove(self, product_id):
        soup = self.get_content()

        product_tag = soup.find("tr", {"id": product_id})
        if product_tag is None:
            raise ProductNotFound()
        product_tag.decompose()

        self._commit(soup)
