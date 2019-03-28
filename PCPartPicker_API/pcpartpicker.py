from ._productsData import productLookup
from json import loads as jsonloads
from bs4 import BeautifulSoup
import requests


def _getRegionURL(region):
    """
    A private function that returns the specific URL for pcpartpicker requests for that
    region
    Supports (case insesetive):
        "au", "be", "ca", "de", "es", "fr", "in", "ie", "it", "nz", "uk", "us"
    """
    region = region.lower()
    if region in [
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
        return (
            "https://" + ((region + ".") if region != "us" else "") + "pcpartpicker.com"
        )
    else:
        raise ValueError(f'"{region}" is an invalid / unrecognized region')


class productLists(object):
    """
    Scrape and retrieve information from pcpartpicker product lists
    For example: https://pcpartpicker.com/products/cpu-cooler/
    """

    @staticmethod
    def _getPage(productType, pageNum=1, region="us"):
        """
        A private method that returns the JSON for that particular page of that
        particular product type
        """
        if productType not in productLookup:
            raise ValueError(
                f'"{productType}" is an invalid / unrecognized productType'
            )

        pcppURL = _getRegionURL(region)
        r = requests.get(
            pcppURL + "/products/" + productType + "/fetch?page=" + str(pageNum)
        )
        parsed = jsonloads(r.content.decode("utf-8"))

        return parsed

    @staticmethod
    def getListInfo(productType, region="us"):
        """
        Returns a dict with the amount of pages for a product, as well as the number of
        products in total in those pages
        """
        data = productLists._getPage(productType, region=region)

        totalProductCount = data["result"]["paging_data"]["total_count"]
        amountOfProductPages = data["result"]["paging_data"]["page_blocks"][-1]["page"]

        return {
            "totalProductCount": totalProductCount,
            "amountOfProductPages": amountOfProductPages,
        }

    @staticmethod
    def _getListHTML(productType, pageNum, region="us"):
        """
        A private method that returns a requests_html HTML object for that particular
        page of that particular product type
        """
        data = productLists._getPage(productType, pageNum, region)
        return BeautifulSoup(data["result"]["html"], "html.parser")

    @staticmethod
    def getList(productType, pageNum=0, region="us"):
        """
        Returns all products for pageNum
        If pageNum is left to default (0), it gets all pages
        The pages start at 1
        """
        if pageNum == 0:
            amountOfProductPages = productLists.getListInfo(productType)[
                "amountOfProductPages"
            ]
            start_pageNum, end_pageNum = 1, amountOfProductPages
        else:
            start_pageNum, end_pageNum = pageNum, pageNum

        productList = []
        for pageNum in range(start_pageNum, end_pageNum + 1):
            soup = productLists._getListHTML(productType, pageNum, region)
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
