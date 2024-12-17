"""Setup configuration for rebirth-launcher."""
from setuptools import setup, find_packages

setup(
    name="rebirth-launcher",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)