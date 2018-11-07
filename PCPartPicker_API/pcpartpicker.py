from json import loads as jsonloads
from ._productsData import productLookup
from bs4 import BeautifulSoup
from requests import get

baseURL = "https://pcpartpicker.com"

def setRegion(region):
    """
    Change the region for the pcpartpicker.com requests. Supports (case insesetive):
    "au", "be", "ca", "de", "es", "fr", "in", "ie", "it", "nz", "uk", "us"
    """
    global baseURL
    region = region.lower()
    if region in ["au", "be", "ca", "de", "es", "fr", "in", "ie", "it", "nz", "uk", "us"]:
        baseURL = "https://" + ((region + ".") if region != "us" else "") + "pcpartpicker.com"
    else:
        raise ValueError("region \"{}\" not supported".format(region))

class productLists(object):
    """
    For scraping product lists such as
    https://pcpartpicker.com/products/cpu-cooler/
    """

    @staticmethod
    def _getPage(partType, pageNum, returnMaxPageNum=False):
        """
        A private method to GET, decode, and parse a page from pcpartpicker
        If returnMaxPageNum is True, this function will only return an Int
        """
        if partType not in productLookup:
            raise ValueError("partType invalid")
        r = get(baseURL + "/products/" + partType + "/fetch?page=" + str(pageNum))
        parsed = jsonloads(r.content.decode("utf-8"))
        if returnMaxPageNum:
            return parsed["result"]["paging_data"]["page_blocks"][-1]["page"]
        return BeautifulSoup(parsed["result"]["html"], "html.parser")
    
    @staticmethod
    def totalPages(partType):
        """
        Returns the total number of pages for partType
        """
        return productLists._getPage(partType, 1, True)

    @staticmethod
    def getProductList(partType, pageNum=0):
        """
        Returns results for pageNum. If pageNum is left to default, get all
        pages. pageNum starts at 1
        """
        if pageNum == 0:
            start_pageNum, end_pageNum = 1, productLists.totalPages(partType)
        else:
            start_pageNum, end_pageNum = pageNum, pageNum

        cpuList = []
        for pageNum in range(start_pageNum, end_pageNum+1):
            soup = productLists._getPage(partType, pageNum)
            for row in soup.find_all("tr"):
                cpuDetails = {}
                for count, value in enumerate(row):
                    text = value.get_text().strip()

                    if count in productLookup[partType]:
                        cpuDetails[productLookup[partType][count]] = text
                    elif count == 1:
                        cpuDetails["name"] = text
                    elif count == len(row)-2:
                        cpuDetails["price"] = text
                    elif count == len(row)-3:
                        cpuDetails["ratings"] = text.replace("(", "").replace(")", "")
                    else:
                        try:
                            if value.a["class"] == ["btn-mds", "pp_add_part"]:
                                cpuDetails["id"] = value.a["href"].replace("#", "")
                        except TypeError:
                            pass  # Not <a> tag
                        except KeyError:
                            pass  # No class

                cpuList.append(cpuDetails)
        return cpuList
