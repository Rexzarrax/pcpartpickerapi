from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

with open(path.join(here, "requirements.txt"), encoding="utf-8") as f:
    requirements = f.read()
    # If on win, get rid of CR
    requirements = requirements.replace("\r", "")
    requirements = requirements.split("\n")

setup(
    name="pcpartpickerapi",
    version="0.1.5",
    description="An unofficial Py3 API to scrape and retrieve information from PCPartPicker",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thatguywiththatname/pcpartpickerapi",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    keywords="pcpartpickerapi api scraping scraper webscraper pcparts",
    packages=find_packages(exclude=["contrib", "docs", "tests", "examples"]),
    install_requires=requirements,
)
