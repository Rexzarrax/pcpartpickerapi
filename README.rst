pcpartpickerapi
===============

Python3 API for scraping and retrieving information from
`PcPartPicker <https://pcpartpicker.com>`__

**What can this API do?**

Currently this library contains these features:

-  The ``part_lists`` file
-  Extract information from pages that are lists of parts, as seen under
   the "browse by individual parts" tab on the PCPartPicker website
   (such as
   `products/cpu-cooler <https://pcpartpicker.com/products/cpu-cooler>`__)
-  All part lists are supported except the ones under the "Software"
   catergory, although those may be supported in the future
-  All regions supported by PCPartPicker are supported and can be
   requested by using the ``region`` paramter in public functions. The
   region defaults to "US"
-  All filters for part lists are supported (explained further in the
   documentation below)

**Note about the words "product" and "part"**

PCPartPicker seems to use these words somewhat interchangeably. For this
API, all PC parts are referred to as "parts"

Installation
------------

``pip install pcpartpickerapi``

See the GitHub page `here <https://github.com/thatguywiththatname/pcpartpickerapi/>`__

Quickstart
----------

.. code:: python

    # Import the part_lists file from the package
    from pcpartpickerapi import part_lists

    # Print the total amount of pages for CPUs
    print("Total CPU pages:", part_lists.get_list_info("cpu")["page_count"])

    # Pull info from page 1 of CPUs
    cpu_info = part_lists.get_list("cpu", page_num=1)

    print(cpu_info[0])

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

Documentation
-------------

The ``pcpartpickerapi`` module contains these (public) files / classes /
functions:

+--------------------------------+----------------------------------------------------------+--------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Function name                  | Paramaters                                               | Returns                                                                  | Notes                                                                                                                                                                                                                 |
+================================+==========================================================+==========================================================================+=======================================================================================================================================================================================================================+
| ``part_lists.get_list``        | ``part_type, page_num=0, region="us", part_filter=""``   | A list of dictionaries containing information about each part            | ``page_num`` is set to ``0`` by default. ``0`` means it will iterate over all available pages.If you only want to get information from, for example, page 2 of the cpu results, you would set ``page_num`` to ``2``   |
+--------------------------------+----------------------------------------------------------+--------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``part_lists.get_list_info``   | ``part_type, region="us", part_filter=""``               | A dictionary with the keys ``"page_count"`` and ``"total_part_count"``   | ``"page_count"`` is the total number of pages for that ``part_type``. ``"total_part_count"`` Is the total number of parts in all of those pages                                                                       |
+--------------------------------+----------------------------------------------------------+--------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

part\_type
~~~~~~~~~~

Some of the functions require a ``part_type`` parameter. This is used to
determine what PC part type (CPU, PSU, etc.) you want to get information
about

If you request a part list using ``part_lists.get_list``, the
``part_type`` you select will decide what dictionary keys will be
available to you for each dictionary in the returned list. For example,
if you select ``"cpu-cooler"`` as your part type, the keys will be
``"fan-rpm"`` and ``"noise level"`` (as well as the default keys)

To see what keys exist for each ``part_type``, you can look them up in
`\_\_partsData <https://github.com/thatguywiththatname/PcPartPicker-API/blob/master/pcpartpickerapi/__parts_data.py>`__

Every dictionary will always contain the default keys ``name``,
``price``, ``ratings`` and ``id`` (although they may not always have a
value).

region
~~~~~~

The default region is ``"us"``. All of these are case insensetive, i.e.
you can use ``"us"`` or ``"US"``, both will work

``"au", "be", "ca", "de", "es", "fr", "in", "ie", "it", "nz", "uk", "us"``

part\_filter
~~~~~~~~~~~~

The ``part_filter`` parameter supports filters used by the PCPP website
(it is not shortened to ``filter`` because that is a built-in function
in Python)

For example, for this URL:
``https://pcpartpicker.com/products/cpu/#k=30&R=4`` the filter is
``k=30&R=4`` (this filters all LGA1151 socket CPUs with 4 or more stars)

To use this you would put it into the ``part_filter`` paramter:

.. code:: python

    part_lists.get_list("cpu", part_filter="k=30&R=4")

If you want to filter for something specific, you will need to visit the
PcPartPicker website and filter it by hand, and then the URL will
contain the filter you want. Using an incorrect filter for this paramter
might cause unexpected errors
