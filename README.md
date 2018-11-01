# PCPartPicker-API

Python3 API for retrieving information from [PcPartPicker](https://pcpartpicker.com)

### What can this do?

Currently this library contains these features:

 - Select what region you want to use ("uk", "ca", etc.)

 - The `productLists` class - for interacting with pages that are lists of products, as seen under the "browse by individual parts" tab on the PCPartPicker website (such as [products/cpu-cooler](https://pcpartpicker.com/products/cpu-cooler)). All product lists are supported except the ones under the `SOFTWARE` catergory, although those may be supported in the future

# Installation

`pip install PCPartPicker_API`

See the PyPi page [here](https://pypi.python.org/pypi/PCPartPicker-API)

# Quickstart

A quick demonstration of what this API can do

```python
# Import pcpartpicker
from PCPartPicker_API import pcpartpicker as pcpp

# Print the total amount of pages for CPUs
print("Total CPU pages:", pcpp.productLists.totalPages("cpu"))

# Pull info from page 1 of CPUs
cpu_info = pcpp.productLists.getList("cpu", 1)

# Print the names and prices of all the CPUs on the page
for cpu in cpu_info:
    print(cpu["name"], ":", cpu["price"])

# Change the region to UK (the default is US)
pcpp.set_region("uk")
print("\nRegion changed to UK")

# Pull info from all CPU pages (this may take a minute)
cpu_info_uk = pcpp.productLists.getList("cpu")

# Print the names and prices of all the CPUs on all pages
# The prices will now be in GBP (£) instead of USD ($)
for cpu in cpu_info_uk:
    print(cpu["name"], ":", cpu["price"])
```

# Documentation

To start using the API, import `pcpartpicker` from `PCPartPicker_API`

A list of `partType`s and their dictionary keys are available in [_productsData](https://github.com/thatguywiththatname/PcPartPicker-API/blob/master/PCPartPicker_API/_productsData.py)

`pcpartpicker` contains these (public) functions:

Function name | Paramaters | Description
-|-|-
`setRegion` | `region` | The region of PCPartPicker that this API uses. `region` must be one of: `"au", "be", "ca", "de", "es", "fr", "in", "ie", "it", "nz", "uk", "us"`. The defualt is for this library is `"us"`. As far as I can tell this only changes the currency
`productLists.getList` | `partType, pageNum=0` | This function returns a list of dictionaries. Each `partType` will have different dictionary keys. To see what keys exist for each `partType`, you can look them up in [_productsData](https://github.com/thatguywiththatname/PcPartPicker-API/blob/master/PCPartPicker_API/_productsData.py). Every dictionary will always contain the keys `name`, `price`, `ratings` and `id` (although they may not always have a value). `pageNum` is set to `0` by default. `0` means it will scrape all pages and gather all the info it can. If you only want to get information from, for example, page 2 of the cpu results, you would set `pageNum` to `2`
`productLists.totalPages` | `partType` | This function simply returns the amount of pages of results there are for a particular `partType`

# ToDo

 - Support the `SOFTWARE` catergory in `pcpartpicker.productLists`
