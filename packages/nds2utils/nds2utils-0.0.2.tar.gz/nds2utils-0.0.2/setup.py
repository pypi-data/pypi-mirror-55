import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nds2utils",
    version="0.0.2",
    author="Craig Cahillane",
    author_email="ccahilla@caltech.edu",
    description="nds2 utilities for reading LIGO data quickly and easily",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.ligo.org/craig-cahillane/nds2utils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
