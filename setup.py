from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["pandas==1.4.1"]

setup(
    name="stockeasy",
    version="0.0.4",
    author="Adam Blacke",
    author_email="adamblacke@gmail.com",
    description="A package for a quick and dirty portfolio analysis.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/AdamBlacke/stockeasy",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
)