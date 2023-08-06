import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="doubleclickcrypto",
    version="0.1",
    author="Daniel Hedrén",
    author_email="danielhedren@gmail.com",
    description="Module for decrypting doubleclick price confirmations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/danielhedren/doubleclickcrypto",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)