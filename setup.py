import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyTexecom",
    version="0.1.5",
    author="James Drew Williams",
    author_email="james@jmtechnical.co.uk",
    description="Texecom Interface Libary",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JDW2018/pyTexecom",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
