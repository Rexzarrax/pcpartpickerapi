# PCPartPicker-API

Python3 API for scraping and retrieving information from [PcPartPicker](https://pcpartpicker.com)

**What can this API do?**

Currently this library contains these features:

- The `productLists` class
  - Extract information from pages that are lists of products, as seen under the "browse by individual parts" tab on the PCPartPicker website (such as [products/cpu-cooler](https://pcpartpicker.com/products/cpu-cooler))
  - All product lists are supported except the ones under the "Software" catergory, although those may be supported in the future
  - All regions supported by PCPartPicker are supported and can be requested by using the `region` paramter in public functions. The region defaults to "US"
  - All filters for product lists are supported (explained further in the documentation below)

**Note about the words "product" and "part"**

PCPartPicker seems to use these words somewhat interchangeably. For this API, I refer to the lists of parts on the website as "product lists", as for referring to individual parts, I refer to them as "parts"

## Installation

`pip install PCPartPicker_API`

See the PyPi page [here](https://pypi.python.org/pypi/PCPartPicker-API)

## Quickstart

```python
# Import pcpartpicker from the package
# Imported here as "pcpp" to makes lines shorter
from PCPartPicker_API import pcpartpicker as pcpp

# Print the total amount of pages for CPUs
print("Total CPU pages:", pcpp.productLists.getListInfo("cpu")["pageCount"])

# Pull info from page 1 of CPUs
cpu_info = pcpp.productLists.getList("cpu", pageNum=1)

# Print the names and prices of all the CPUs on the page
for cpu in cpu_info:
    print(cpu["name"], ":", cpu["price"])

# Pull info from all CPU pages (this may take a minute)
# Also pull this info from the UK region of the site
cpu_info_uk = pcpp.productLists.getList("cpu", region="uk")

# Print the names and prices of all the CPUs on all pages
# The prices will now be in GBP (£) instead of USD ($)
for cpu in cpu_info_uk:
    print(cpu["name"], ":", cpu["price"])
```

## Documentation

To start using the API, import the `pcpartpicker` file from the `PCPartPicker_API` module

The `pcpartpicker` file contains these (public) classes / functions:

Function name | Paramaters | Returns | Notes
-|-|-|-
`productLists.getList` | `partType, pageNum=0, region="us", partFilter=""` | A list of dictionaries containing information about each part | `pageNum` is set to `0` by default. `0` means it will iterate over all available pages.If you only want to get information from, for example, page 2 of the cpu results, you would set `pageNum` to `2`
`productLists.getListInfo` | `partType, region="us", partFilter=""` | A dictionary with the keys `"pageCount"` and `"totalPartCount"` | `"pageCount"` is the total number of pages for that `partType`. `"totalPartCount"` Is the total number of parts in all of those pages

### partType

Some of the functions require a `partType` parameter. This is used to determine what PC part type (CPU, PSU, etc.) you want to get information about

If you request a product list using `productLists.getList`, the `partType` you select will decide what dictionary keys will be available to you for each dictionary in the returned list. For example, if you select `"cpu-cooler"` as your part type, the keys will be `"fan-rpm"` and `"noise level"` (as well as the default keys)

To see what keys exist for each `partType`, you can look them up in [__partsData](https://github.com/thatguywiththatname/PcPartPicker-API/blob/master/PCPartPicker_API/__partsData.py)

Every dictionary will always contain the default keys `name`, `price`, `ratings` and `id` (although they may not always have a value).

### region

The default region is `"us"`. All of these are case insensetive, i.e. you can use `"us"` or `"US"`, both will work

`"au", "be", "ca", "de", "es", "fr", "in", "ie", "it", "nz", "uk", "us"`

### partFilter

The `partFilter` parameter supports filters used by the PCPP website (it is not shortened to `filter` because that is a built-in function in Python)

For example, for this URL: 

https://pcpartpicker.com/products/cpu/#k=30&R=4

the filter is `k=30&R=4` (this filters all LGA1151 socket CPUs with 4 or more stars)

To use this you would put it into the `partFilter` paramter

`pcpp.productLists.getList("cpu", partFilter="k=30&R=4")`

If you want to filter for something specific, you will need to visit the PcPartPicker website and filter it by hand, and then the URL will contain the filter you want
