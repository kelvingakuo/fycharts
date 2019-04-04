import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fycharts",
    version="1.2.0",
    author="Kelvin Gakuo",
    author_email="kelvingakuo@gmail.com",
    description="A fully-fledged installable python package for extracting top 200 and viral 50 charts off of spotifycharts.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kelvingakuo/fycharts",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)