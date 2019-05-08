"""
Scrape and retrieve information from pcpartpicker part lists
For example: https://pcpartpicker.com/products/cpu-cooler/
"""

from .__parts_data import part_type_column_names
from json import loads as jsonloads
import pandas as pd
import requests

supported_part_types = list(part_type_column_names.keys())
supported_regions = [
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
]


def __construct_url(part_type, page, region, part_filter):
    """
    Returns the specific pcpartpicker URL for the given parameters
    """
    region = region.lower()

    # TODO: Is this the best place to do these checks?
    if region not in supported_regions:
        raise ValueError(f'"{region}" is an invalid / unrecognized region')

    if part_type not in supported_part_types:
        raise ValueError(f'"{part_type}" is an invalid / unrecognized part_type')

    pcpp_url = (
        "https://" + ("" if region == "us" else (region + ".")) + "pcpartpicker.com"
    )

    pcpp_url += f"/products/{part_type}/fetch/?page={page}"

    if part_filter.strip() != "":
        pcpp_url += f"&{part_filter}"

    return pcpp_url


def __get_json(part_type, page, region, part_filter):
    """
    Returns the JSON from pcpartpicker for the given parameters
    """
    pcpp_url = __construct_url(part_type, page, region, part_filter)
    r = requests.get(pcpp_url)
    return jsonloads(r.content.decode("utf-8"))


def list_info(part_type, region="us", part_filter=""):
    """
    Returns a dictionary with information about the chosen part list
    """
    data = __get_json(part_type, 1, region, part_filter)

    total_part_count = data["result"]["paging_data"]["total_count"]
    page_count = data["result"]["paging_data"]["page_blocks"][-1]["page"]

    return {"total_part_count": total_part_count, "page_count": page_count}


def get_list(part_type, page=0, region="us", part_filter=""):
    """
    Returns a list of dictionaries containing information about each part
    If page is left to the default (0), it gets all pages
    The pages start at 1
    """
    if page == 0:
        part_page_count = list_info(part_type, region, part_filter)["page_count"]
        start_page, end_page = 1, part_page_count
    else:
        start_page, end_page = page, page

    column_names = part_type_column_names[part_type]
    part_dict_list = []

    for page in range(start_page, end_page + 1):

        data = __get_json(part_type, page, region, part_filter)

        html_table = f"<table>{data['result']['html']}</table>"

        table_df = pd.read_html(html_table)[0]
        # Replace "NaN" values with None
        table_df = table_df.replace({pd.np.nan: None})

        table_row_count = table_df.shape[0]
        table_dict = table_df.to_dict()

        for row_num in range(table_row_count):

            part_dict = {}

            for col_num in range(len(column_names)):

                col_name = column_names[col_num]

                # +1 because the 0th column is the row number
                col_value = table_dict[col_num + 1][row_num]

                # TODO: Is this the best way to do this?
                if col_name == "ratings_count":
                    # Remove "()" from the ratings count
                    col_value = col_value.replace("(", "")
                    col_value = col_value.replace(")", "")

                part_dict[col_name] = col_value

            part_dict_list.append(part_dict)

    return part_dict_list


def supported_keys(part_type):
    """
    Returns a list of dictionary keys that the dictionaries from get_list will have
    for that part_type
    """
    return part_type_column_names[part_type]
