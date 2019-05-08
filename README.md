# pcpartpickerapi

Python3 API for scraping and retrieving information from [PcPartPicker](https://pcpartpicker.com)

### What can this API do?

Currently this library contains these features:

- The `part_lists` file
  - Extract information from pages that are lists of parts, as seen under the "browse by individual parts" tab on the PCPartPicker website (such as [products/cpu-cooler](https://pcpartpicker.com/products/cpu-cooler))
  - All part lists are supported except the ones under the "Software" catergory, although those may be supported in the future
  - All regions supported by PCPartPicker are supported and can be requested by using the `region` paramter in public functions. The region defaults to "US"
  - All filters for part lists are supported (explained further in the documentation below)

A quick note about the words "product" and "part", PCPartPicker seems to use these words somewhat interchangeably. For this API, all PC parts are referred to as "parts"

## Installation

`pip install pcpartpickerapi`

See the PyPi page [here](https://pypi.org/project/pcpartpickerapi/)

## Quickstart

```python
from pcpartpickerapi import part_lists

cpu_list_info = part_lists.list_info("cpu")
print("Total amount of CPU pages:", cpu_list_info["page_count"])

# Pull info from page 1 of CPUs
cpu_info = part_lists.get_list("cpu", page=1)

# Print the names and prices of all the CPUs on the page
for cpu in cpu_info:
    print(cpu["name"], ":", cpu["price"])

# Pull info from all CPU pages (this may take a minute)
# Also pull this info from the UK region of the site
cpu_info_uk = part_lists.get_list("cpu", region="uk")

# Print the names and prices of all the CPUs on all pages
# The prices will now be in GBP (£) instead of USD ($)
for cpu in cpu_info_uk:
    print(cpu["name"], ":", cpu["price"])
```

## Documentation

The `pcpartpickerapi` module contains these (public) files / classes / functions:

Name | Type | Paramaters | Returns / Type | Notes
-|-|-|-|-
`part_lists.get_list` | Function | `part_type, page=0, region="us", part_filter=""` | List | Returns a list of dictionaries containing information about each part. The `part_type` you select will determine what dictionary keys will be available to you for each dictionary in the returned list. If `page` is `0` it will iterate over all available pages
`part_lists.list_info` | Function | `part_type, region="us", part_filter=""` | A dictionary with the keys `"page_count"` and `"total_part_count"` | `"page_count"` is the total number of pages for that `part_type`. `"total_part_count"` Is the total number of parts in all of those pages
`part_lists.supported_part_types` | Variable | | List | A list of supported `part_type`s
`part_lists.supported_regions` | Variable | | List | A list of supported regions
`part_lists.supported_keys` | Function | `part_type` | List | Returns a list of dictionary keys that the dictionaries from `get_list` will have when called with that `part_type`, e.g. `supported_keys("cpu")` will return `["name", "speed", "cores", "tdp", "ratings_count", "price"]`

### Parameter Explanations

#### part_type

This is what PC part type (`"cpu"`, `"cpu-cooler"`, etc.) you want to get information about

#### part_filter

The `part_filter` parameter supports filters used by the PCPP website (it is not shortened to `filter` because that is a built-in function in Python)

For example, for this URL: `https://pcpartpicker.com/products/cpu/#k=30&R=4` the filter is `k=30&R=4` (this filters all LGA1151 socket CPUs with 4 or more stars)

To use this you would put it into the `part_filter` paramter:

```python
part_lists.get_list("cpu", part_filter="k=30&R=4")
```

If you want to filter for something specific, you will need to visit the PcPartPicker website and filter it by hand, and then the URL will contain the filter you want. Using an incorrect filter for this paramter might cause unexpected errors
