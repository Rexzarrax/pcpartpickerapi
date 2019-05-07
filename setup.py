from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pcpartpickerapi",
    version="0.1.5",
    description="An unofficial Py3 API to scrape and retrieve information from PCPartPicker",
    long_description=long_description,
    url="https://github.com/thatguywiththatname/pcpartpickerapi",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    keywords="pcpartpickerapi api scraping scraper pcparts",
    packages=find_packages(exclude=["contrib", "docs", "tests", "examples"]),
    install_requires=["beautifulsoup4", "requests"],
)
