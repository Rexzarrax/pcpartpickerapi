PCPartPicker-API
================

Python3 API for scraping and retrieving information from
`PcPartPicker <https://pcpartpicker.com>`__

**What can this API do?**

Currently this library contains these features:

-  Extract information from pages that are lists of products, as seen
   under the "browse by individual parts" tab on the PCPartPicker
   website (such as
   `products/cpu-cooler <https://pcpartpicker.com/products/cpu-cooler>`__)
-  All product lists are supported except the ones under the "Software"
   catergory, although those may be supported in the future
-  All regions supported by PCPartPicker are supported (au, be, ca, de,
   es, fr, in, ie, it, nz, uk, us) and can be requested by using the
   ``region`` paramter in public functions. The region defaults to "US"
-  All filters for product lists are supported (explained further in the
   documentation below)

Installation
------------

``pip install PCPartPicker_API``

See the GitHub page
`here <https://github.com/thatguywiththatname/PCPartPicker-API>`__

Quickstart
----------

.. code:: python

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

Documentation
-------------

To start using the API, import ``pcpartpicker`` from
``PCPartPicker_API``

A list of ``partType``\ s and their dictionary keys are available in
`\_productsData <https://github.com/thatguywiththatname/PcPartPicker-API/blob/master/PCPartPicker_API/_productsData.py>`__

``pcpartpicker`` contains these (public) functions:

+--------------------------------+----------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Function name                  | Paramaters                                               | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
+================================+==========================================================+===================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================+
| ``productLists.getList``       | ``partType, pageNum=0, region="us", productFilter=""``   | This function returns a list of dictionaries. Each ``partType`` will have different dictionary keys. To see what keys exist for each ``partType``, you can look them up in `\_productsData <https://github.com/thatguywiththatname/PcPartPicker-API/blob/master/PCPartPicker_API/_productsData.py>`__. Every dictionary will always contain the keys ``name``, ``price``, ``ratings`` and ``id`` (although they may not always have a value). ``pageNum`` is set to ``0`` by default. ``0`` means it will iterate over all available pages.If you only want to get information from, for example, page 2 of the cpu results, you would set ``pageNum`` to ``2``   |
+--------------------------------+----------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``productLists.getListInfo``   | ``partType, region="us", productFilter=""``              | Returns a dict with the amount of pages for a product, as well as the number of products in total in those pages. The keys are ``"totalProductCount"`` and ``pageCount``                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
+--------------------------------+----------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

Supported regions (case insensetive)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``"au", "be", "ca", "de", "es", "fr", "in", "ie", "it", "nz", "uk", "us"``

productFilter
~~~~~~~~~~~~~

The ``productFilter`` parameter supports filters used by the PCPP
website. For example, for this URL:

https://pcpartpicker.com/products/cpu/#k=30&R=4

the filter is ``k=30&R=4`` (this filters all LGA1151 socket CPUs with 4
stars)

To use this you would put it into the ``productFilter`` paramter

``pcpp.productLists.getList("cpu", productFilter="k=30&R=4")``

If you want to filter for something specific, you will need to visit the
PcPartPicker website and filter it by hand, and then the URL will
contain the filter you want
