from setuptools import setup
from setuptools import find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="quintagroup.xmlsec.init",
    version="0.2.0",
    description="A simple package for dm.xmlsec.binding initialization",
    author="Taras Dyshkant",
    author_email="hitori@quintagroup.org",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/quintagroup/quintagroup.xmlsec.init",
    packages=find_packages(),
    namespace_packages=["quintagroup",
                        "quintagroup.xmlsec",
    ],
    install_requires=["setuptools",
                      "dm.xmlsec.binding>=2.0",
                      "zope.component",
    ],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points="""
    # -*- Entry points: -*-
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
