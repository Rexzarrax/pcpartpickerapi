"""
Scrape and retrieve information from pcpartpicker part lists
For example: https://pcpartpicker.com/products/cpu-cooler/
"""

from .__parts_data import part_lookup
from json import loads as jsonloads
from bs4 import BeautifulSoup, NavigableString
import requests


def __construct_url(part_type, page_num, region, part_filter):
    """
    Returns the specific pcpartpicker URL for the given parameters
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

    pcpp_url = (
        "https://" + ("" if region == "us" else (region + ".")) + "pcpartpicker.com"
    )

    pcpp_url += f"/products/{part_type}/fetch/?page={page_num}"

    if part_filter.strip() != "":
        pcpp_url += f"&{part_filter}"

    return pcpp_url


def __get_json(part_type, page_num, region, part_filter):
    """
    Returns the JSON from pcpartpicker for the given parameters
    """
    if part_type not in part_lookup:
        raise ValueError(f'"{part_type}" is an invalid / unrecognized part_type')

    pcpp_url = __construct_url(part_type, page_num, region, part_filter)
    r = requests.get(pcpp_url)
    parsed = jsonloads(r.content.decode("utf-8"))

    return parsed


def __get_list_html(part_type, page_num, region, part_filter):
    """
    Returns a BeautifulSoup object for the page for the given parameters
    """
    data = __get_json(part_type, page_num, region, part_filter)
    return BeautifulSoup(data["result"]["html"], "html.parser")


def list_info(part_type, region="us", part_filter=""):
    """
    Returns a dictionary with information about the chosen part list
    """
    data = __get_json(part_type, 1, region, part_filter)

    total_part_count = data["result"]["paging_data"]["total_count"]
    page_count = data["result"]["paging_data"]["page_blocks"][-1]["page"]

    return {"total_part_count": total_part_count, "page_count": page_count}


def get_list(part_type, page_num=0, region="us", part_filter=""):
    """
    Returns a list of dictionaries containing information about each part
    If page_num is left to the default (0), it gets all pages
    The pages start at 1
    """
    if page_num == 0:
        part_page_count = list_info(part_type, region, part_filter)["page_count"]
        start_page_num, end_page_num = 1, part_page_count
    else:
        start_page_num, end_page_num = page_num, page_num

    part_dict_list = []
    for page_num in range(start_page_num, end_page_num + 1):

        # For each page requested, get the bs4 soup for that page
        soup = __get_list_html(part_type, page_num, region, part_filter)

        # For each row in the table, pull the known data
        for row in soup.find_all("tr"):

            part_details = {}
            for count, value in enumerate(row):

                # Each part has a HTML table that contains the information about it.
                # Some rows don't matter, and others have a value. The ones with values
                # always have a value, and for each partType, contain specific data.
                # For example, the 3rd row for any part always contains the parts name.
                # The part_lookup dict contains {row number : data name} pairs that
                # allow you to determine what row contains what data.

                if isinstance(value, NavigableString):
                    continue  # Skip blank strings

                text = value.get_text().strip()

                if count in part_lookup[part_type]:
                    part_details[part_lookup[part_type][count]] = text

                elif count == 1:
                    part_details["id"] = value.input["id"]
                elif count == 3:
                    part_details["name"] = text
                elif count == len(row) - 3:
                    part_details["price"] = text
                elif count == len(row) - 5:
                    # The rating counts are surrounded by ()
                    part_details["ratings_count"] = text.replace("(", "").replace(
                        ")", ""
                    )

            part_dict_list.append(part_details)

    return part_dict_list


def supported_part_types():
    """
    Returns a list of supported part_types
    """
    return list(part_lookup.keys())


def supported_keys(part_type):
    """
    Returns a list of dictionary keys that the dictionaries from get_list will have
    for that part_type
    """
    keys = list(part_lookup[part_type].values())
    keys.append("name")
    keys.append("id")
    keys.append("price")
    keys.append("ratings_count")
    return keys
