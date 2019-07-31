import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# The nisaba version
nisaba_version = "0.2.7"

# This call to setup() does all the work
setup(
    name="nisaba",
    version=nisaba_version,
    description="A tool for multi-modal annotation",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/mhbeals/nisaba",
    download_url = 'https://github.com/mhbeals/nisaba/archive/' + nisaba_version + '.tar.gz',
    author="M. H. Beals",
    author_email="M.H.Beals@lboro.ac.uk",
    license="AGPLv3",
    classifiers=[
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    py_modules=["nisaba"],
    packages=["nisaba"],
    include_package_data=True,
    install_requires=["isodate", "Pillow", "pyparsing", "rdflib", "six", "ttkwidgets"],
    entry_points={
        "console_scripts": [
            "nisaba=nisaba.__main__:main",
        ]
    },
)
