import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bidq",
    version="0.0.1",
    author="Alon Niv",
    author_email="oakfang@gmail.com",
    description="Python SDK for bidq",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bidq/pybidq",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)