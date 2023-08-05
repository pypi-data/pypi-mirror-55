from distutils.core import setup
from pathlib import Path
from setuptools import find_packages


HERE = Path(__file__).parent

README = (HERE / "README.md").read_text()


def get_requirements():
    with Path("requirements.txt").open("r") as f:
        return f.readlines()


setup(
    name="geo_places",
    version="0.0.4",
    description="A bunch of utilities for working with czech municipalities",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Jiri Bauer",
    author_email="baueji@gmail.com",
    url="https://github.com/bauerji/geo_locations.git",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    install_requires=get_requirements(),
    python_requires=">=3.7",
    data_files=[("data", ["data/municipality_population.csv"])],
)
