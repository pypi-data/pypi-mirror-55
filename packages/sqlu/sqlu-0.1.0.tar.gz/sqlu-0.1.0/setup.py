import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sqlu",
    version="0.1.0",
    author="Matteo Redaelli",
    author_email="matteo.redaelli@gmail.com",
    description="sqlu is a simple utility for transforming or extracting info from sql statements",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/matteo.redaelli/sqlu",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['flatten_json', 'moz_sql_parser'],
    python_requires='>=3.6',
)
