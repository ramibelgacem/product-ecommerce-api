from bs4 import BeautifulSoup


class HtmlORM:
    def __init__(self, filename):
        self.filename = filename

    def add(self, product):
        html = open(self.filename)
        soup = BeautifulSoup(html, "html.parser")

        table = soup.find("table", {"id": "productsInfo"})
        table.append(
            BeautifulSoup(
                f"<tr><td>{product.id}</td><td>{product.name}</td>"
                f"<td>{product.description}</td><td>{product.price}</td></tr>",
                "html.parser",
            )
        )

        with open(self.filename, "wb") as f_output:
            f_output.write(soup.prettify("utf-8"))
