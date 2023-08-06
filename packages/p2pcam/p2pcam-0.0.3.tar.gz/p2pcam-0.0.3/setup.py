import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="p2pcam",
    version="0.0.3",
    author="IndyKoning",
    description="A package to talk to p2p cameras",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/indykoning/PyPI_p2pcam",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
