# coding: utf-8

"""
    VTPL API Wrapper and VTPL Video Stream
"""


from setuptools import setup, find_packages  # noqa: H301

NAME = "vtpl-api-wrapper"
VERSION = "1.0.6"

REQUIRES = ["opencv-python>=4.1", "PyYAML", "requests", "vtpl-api==1.0.4"]

setup(
    name=NAME,
    version=VERSION,
    description="VTPL API Wrapper and VTPL Video Stream",
    author_email="",
    url="",
    keywords=[
        "vtpl",
        "VTPL",
        "Videonetics",
        "Videonetics OpenAPI",
        "OpenAPI",
        "VTPL API Wrapper",
        "Videonetics API Wrapper",
        "VTPL API Wrapper",
        "VTPL Video Stream",
        "Videonetics Video Stream"
    ],
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
    long_description="""\
    VTPL API Wrapper and VTPL Video Stream
    """
)
