import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fycharts",
    version="4.0.2",
    author="Kelvin Gakuo",
    author_email="kelvingakuo@gmail.com",
    description="A fully-fledged installable python package for extracting top 200 and viral 50 charts off of spotifycharts.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kelvingakuo/fycharts",
    packages=setuptools.find_packages(),
    install_requires=[
        "pandas==1.1.2",
        "requests==2.24.0",
        "click==7.1.2",
        "colorama==0.4.3"
    ],
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points = """
		[console_scripts]
		fycharts=fycharts.cli:main
	"""
)