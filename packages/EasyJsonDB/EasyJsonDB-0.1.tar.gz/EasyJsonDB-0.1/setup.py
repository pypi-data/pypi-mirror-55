import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="EasyJsonDB", # Replace with your own username
    version="0.1",
    author="vlnerable",
    author_email="vlnerablehacking@gmail.com",
    description="A simple db script for everyone to use it",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vlnerable/EasyDB",
    packages=[
      "EasyJsonDB",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)