# PCPartPicker-API

Python3 API for getting part information from [PcPartPicker](https://uk.pcpartpicker.com)

Everything is pulled directly from there, no data is stored in this package

# Installation

`pip install PCPartPicker_API`

# Quickstart

```python
# Import PPP_API
from PCPartPicker_API import PCPartPicker

# Print the total amount of pages for CPUs
print("Total CPU pages:", PCPartPicker.get_total_pages("cpu"))

# Pull info from page 2
cpu_info = PCPartPicker.get_part("cpu", 2)

# Print the names of all the CPUs on page 2
for cpu in cpu_info:
    print(cpu["name"], ":", cpu["price"])
```

# Documentation

To start using the API, import `PCPartPicker` from `PCPartPicker_API` (`from PCPartPicker_API import PCPartPicker`)

`PCPartPicker` contains 2 public functions: `get_part` and `get_total_pages`:

Function name | Paramaters | Description
-|-|-
`get_part` | `part_type, single_page=False` |This function returns a list of dictionaries, Each dictionary contains several different keys & values. To see what keys exist you can either print out the dictionary or just look up what keys there will be for your `part_type` in [_PPP_data](https://github.com/thatguywiththatname/PcPartPicker-API/blob/master/PCPartPicker_API/_PPP_data.py). Every dictionary will always contain the keys `name`, `price` and `ratings` (although they may not always have a value).`part_type` is your PC part type, for example `cpu` or `cpu-cooler`. A list of these parts are in [_PPP_data](https://github.com/thatguywiththatname/PcPartPicker-API/blob/master/PCPartPicker_API/_PPP_data.py). `single_page` is set to `False` by default. `False` means it will scrape all pages and gather all the info it can. If you only want to get information from, for example, page 2 of the cpu results, you would set `single_page` to `2`
`get_total_pages` | `part_type` | This function simply returns the amount of pages of results there are for a particular `part_type`

**[Examples](https://github.com/thatguywiththatname/PcPartPicker-API/tree/master/examples)**
