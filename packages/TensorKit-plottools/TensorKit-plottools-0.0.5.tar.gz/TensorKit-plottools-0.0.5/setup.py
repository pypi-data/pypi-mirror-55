from setuptools import setup
from setuptools import find_packages


setup(
    name="TensorKit-plottools",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
)
