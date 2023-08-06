from setuptools import setup


NAME = "parselx"
DESCRIPTION = (
    "Enhanced version of parsel, extracting data from HTML and XML using complex rules"
)
URL = "https://github.com/wooddance/aCrawler"
EMAIL = "zireael.me@gmail.com"
AUTHOR = "wooddance"
VERSION = "0.0.1"
REQUIRED = ["parsel"]

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=open("README.md").read(),
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    python_requires=">=3.6.0",
    install_requires=REQUIRED,
    packages=["parselx"],
)
