from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="buff163-unofficial-api",
    version="0.1.2",
    author="Mark Zhdan",
    author_email="markzhdan@gmail.com",
    description="An unofficial API wrapper for Buff163, a CS skin marketplace.",
    url="https://github.com/markzhdan/buff163-unofficial-api",
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
