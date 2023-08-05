import setuptools

with open("README.md", "r") as file:
    long_description = file.read()

setuptools.setup(
    name="pack_carlist",
    version="0.0.1",
    author="mvsa",
    author_email="daniel.galea@xomnia.com",
    description="Training example on how to upload package to PyPi",
    long_description=long_description,
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.6"
)