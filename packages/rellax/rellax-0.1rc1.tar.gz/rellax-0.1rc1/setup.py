# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""


import re
from setuptools import setup


version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('rellax/rellax.py').read(),
    re.M
    ).group(1)


with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")


setup(
    name = "rellax",
    packages = ["rellax"],
    entry_points = {
        "console_scripts": ['rellax = rellax.rellax:main']
        },
    version = version,
    description = "Command Line short term knowledgebase management system.",
    long_description = long_descr,
    long_description_content_type='text/markdown',
    author = "Jerrad Anderson",
    author_email = "",
    install_requires = [
        "prompt-toolkit==1.0.15",
        "colored==1.4.0",
        "inquirer==2.6.3",
        "tabulate==0.8.3"]
    )
