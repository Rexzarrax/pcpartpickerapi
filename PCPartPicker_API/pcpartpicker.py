from .__partsData import partLookup
from json import loads as jsonloads
from bs4 import BeautifulSoup
import requests


def __constructURL(region, partFilter):
    """
    A private function that returns the specific URL for pcpartpicker requests for that
    region with that product filter
    Supports these regions (case insesetive):
        "au", "be", "ca", "de", "es", "fr", "in", "ie", "it", "nz", "uk", "us"
    The filter should be in a format like this:
        partFilter = "k=30&R=4,3,0&m=21&f=85,75"
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

    if partFilter.strip() != "":
        pcppURL = f"{pcppURL}/#{partFilter}"

    return pcppURL


class productLists(object):
    """
    Scrape and retrieve information from pcpartpicker product lists
    For example: https://pcpartpicker.com/products/cpu-cooler/
    """

    @staticmethod
    def __getPage(productType, pageNum=1, region="us", partFilter=""):
        """
        A private method that returns the JSON for that particular page of that
        particular product type with that particular partFilter
        """
        if productType not in partLookup:
            raise ValueError(
                f'"{productType}" is an invalid / unrecognized productType'
            )

        pcppURL = __constructURL(region, partFilter)
        r = requests.get(
            pcppURL + "/products/" + productType + "/fetch?page=" + str(pageNum)
        )
        parsed = jsonloads(r.content.decode("utf-8"))

        return parsed

    @staticmethod
    def getListInfo(productType, region="us", partFilter=""):
        """
        Returns a dict with the amount of pages for a product (pageCount), as well as
        the number of parts in total in those pages (totalPartCount)
        """
        data = productLists.__getPage(productType, region=region, partFilter=partFilter)

        totalPartCount = data["result"]["paging_data"]["total_count"]
        pageCount = data["result"]["paging_data"]["page_blocks"][-1]["page"]

        return {"totalPartCount": totalPartCount, "pageCount": pageCount}

    @staticmethod
    def __getListHTML(productType, pageNum, region="us", partFilter=""):
        """
        A private method that returns a requests_html HTML object for that particular
        page of that particular product type with that particular partFilter
        """
        data = productLists.__getPage(productType, pageNum, region, partFilter)
        return BeautifulSoup(data["result"]["html"], "html.parser")

    @staticmethod
    def getList(productType, pageNum=0, region="us", partFilter=""):
        """
        Returns all products for pageNum in region with partFilter
        If pageNum is left to default (0), it gets all pages
        The pages start at 1
        """
        if pageNum == 0:
            amountOfProductPages = productLists.getListInfo(
                productType, region, partFilter
            )["pageCount"]
            start_pageNum, end_pageNum = 1, amountOfProductPages
        else:
            start_pageNum, end_pageNum = pageNum, pageNum

        productList = []
        for pageNum in range(start_pageNum, end_pageNum + 1):
            soup = productLists.__getListHTML(productType, pageNum, region, partFilter)
            for row in soup.find_all("tr"):
                productDetails = {}
                for count, value in enumerate(row):
                    text = value.get_text().strip()

                    if count in partLookup[productType]:
                        productDetails[partLookup[productType][count]] = text
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
