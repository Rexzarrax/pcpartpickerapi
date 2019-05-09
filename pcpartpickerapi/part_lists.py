"""
Scrape and retrieve information from pcpartpicker part lists
For example: https://pcpartpicker.com/products/cpu-cooler/
"""

from .__parts_data import part_type_column_names
from json import loads as jsonloads
import pandas as pd
import threading
import requests
import queue

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


def supported_keys(part_type):
    """
    Returns a list of dictionary keys that the dictionaries from get_list will have
    for that part_type
    """
    part_type = part_type.strip().lower()
    if part_type not in supported_part_types:
        raise ValueError(f'"{part_type}" is an invalid / unrecognized part_type')
    return part_type_column_names[part_type]


def __split_list(a, n):
    """
    Split the list a into n number of sub lists
    https://stackoverflow.com/a/2135920/6396652
    """
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m) : (i + 1) * k + min(i + 1, m)] for i in range(n))


def __construct_url(part_type, page, region, part_filter):
    """
    Returns the specific pcpartpicker URL for the given parameters
    """
    part_type = part_type.strip().lower()
    region = region.strip().lower()

    if part_type not in supported_part_types:
        raise ValueError(f'"{part_type}" is an invalid / unrecognized part_type')

    if region not in supported_regions:
        raise ValueError(f'"{region}" is an invalid / unrecognized part_type')

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


def __dl_and_parse_pages(
    part_type, start_page, end_page, region, part_filter, return_queue=None
):
    """
    Download and parse the part list pages from start_page to end_page (inclusive)
    """
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

                # Remove "()" from the ratings count
                if col_name == "ratings_count":
                    col_value = col_value.replace("(", "")
                    col_value = col_value.replace(")", "")

                part_dict[col_name] = col_value

            part_dict_list.append(part_dict)

    if return_queue:
        return_queue.put(part_dict_list)
    else:
        return part_dict_list


def get_list(
    part_type, page=0, region="us", part_filter="", use_threading=False, thread_count=4
):
    """
    Returns a list of dictionaries containing information about each part
    The pages start at 1
    If page is left to the default (0), it gets all pages
    """
    if page != 0:
        return __dl_and_parse_pages(part_type, page, page, region, part_filter)

    else:
        page_count = list_info(part_type, region, part_filter)["page_count"]

        if not use_threading or thread_count == 1 or thread_count < 0:
            return __dl_and_parse_pages(part_type, 1, page_count, region, part_filter)

        else:
            if thread_count == 0 or thread_count > page_count:
                thread_count = page_count

            pages = [p for p in range(1, page_count + 1)]
            page_chunks = list(__split_list(pages, thread_count))

            threads = []
            return_queue = queue.Queue()
            for page_chunk in page_chunks:
                t = threading.Thread(
                    target=__dl_and_parse_pages,
                    args=(
                        part_type,
                        page_chunk[0],
                        page_chunk[-1],
                        region,
                        part_filter,
                        return_queue,
                    ),
                )
                t.daemon = True
                threads.append(t)
                t.start()

            for t in threads:
                t.join()

            return return_queue.get()
