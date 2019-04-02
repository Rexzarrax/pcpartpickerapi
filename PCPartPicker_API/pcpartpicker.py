from ._productsData import productLookup
from json import loads as jsonloads
from bs4 import BeautifulSoup
import requests


def _constructURL(region, productFilter):
    """
    A private function that returns the specific URL for pcpartpicker requests for that
    region with that product filter
    Supports these regions (case insesetive):
        "au", "be", "ca", "de", "es", "fr", "in", "ie", "it", "nz", "uk", "us"
    The filter should be in a format like this:
        productFilter = "k=30&R=4,3,0&m=21&f=85,75"
    """
    region = region.lower()
    if region not in [
        "au",
        "be",
        "ca",
        "de",
        "es",
        "fr",
        "in",
        "ie",
        "it",
        "nz",
        "uk",
        "us",
    ]:
        raise ValueError(f'"{region}" is an invalid / unrecognized region')

    pcppURL = (
        "https://" + ((region + ".") if region != "us" else "") + "pcpartpicker.com"
    )

    if productFilter.strip() != "":
        pcppURL = f"{pcppURL}/#{productFilter}"

    return pcppURL


class productLists(object):
    """
    Scrape and retrieve information from pcpartpicker product lists
    For example: https://pcpartpicker.com/products/cpu-cooler/
    """

    @staticmethod
    def _getPage(productType, pageNum=1, region="us", productFilter=""):
        """
        A private method that returns the JSON for that particular page of that
        particular product type with that particular productFilter
        """
        if productType not in productLookup:
            raise ValueError(
                f'"{productType}" is an invalid / unrecognized productType'
            )

        pcppURL = _constructURL(region, productFilter)
        r = requests.get(
            pcppURL + "/products/" + productType + "/fetch?page=" + str(pageNum)
        )
        parsed = jsonloads(r.content.decode("utf-8"))

        return parsed

    @staticmethod
    def getListInfo(productType, region="us", productFilter=""):
        """
        Returns a dict with the amount of pages for a product (pageCount), as well as
        the number of products in total in those pages (totalProductCount)
        """
        data = productLists._getPage(
            productType, region=region, productFilter=productFilter
        )

        totalProductCount = data["result"]["paging_data"]["total_count"]
        pageCount = data["result"]["paging_data"]["page_blocks"][-1]["page"]

        return {"totalProductCount": totalProductCount, "pageCount": pageCount}

    @staticmethod
    def _getListHTML(productType, pageNum, region="us", productFilter=""):
        """
        A private method that returns a requests_html HTML object for that particular
        page of that particular product type with that particular productFilter
        """
        data = productLists._getPage(productType, pageNum, region, productFilter)
        return BeautifulSoup(data["result"]["html"], "html.parser")

    @staticmethod
    def getList(productType, pageNum=0, region="us", productFilter=""):
        """
        Returns all products for pageNum in region with productFilter
        If pageNum is left to default (0), it gets all pages
        The pages start at 1
        """
        if pageNum == 0:
            amountOfProductPages = productLists.getListInfo(
                productType, region, productFilter
            )["pageCount"]
            start_pageNum, end_pageNum = 1, amountOfProductPages
        else:
            start_pageNum, end_pageNum = pageNum, pageNum

        productList = []
        for pageNum in range(start_pageNum, end_pageNum + 1):
            soup = productLists._getListHTML(
                productType, pageNum, region, productFilter
            )
            for row in soup.find_all("tr"):
                productDetails = {}
                for count, value in enumerate(row):
                    text = value.get_text().strip()

                    if count in productLookup[productType]:
                        productDetails[productLookup[productType][count]] = text
                    elif count == 1:
                        productDetails["name"] = text
                    elif count == len(row) - 2:
                        productDetails["price"] = text
                    elif count == len(row) - 3:
                        productDetails["ratings"] = text.replace("(", "").replace(
                            ")", ""
                        )
                    else:
                        try:
                            if value.a["class"] == ["btn-mds", "pp_add_part"]:
                                productDetails["id"] = value.a["href"].replace("#", "")
                        except TypeError:
                            pass  # Not <a> tag
                        except KeyError:
                            pass  # No class

                productList.append(productDetails)
        return productList
