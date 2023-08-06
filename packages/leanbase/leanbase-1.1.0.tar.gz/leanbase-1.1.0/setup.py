import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

print(long_description)

setuptools.setup(
    name="leanbase",
    version="1.1.0",
    author="Dipanjan Mukherjee",
    author_email="dipanjan@leanbase.io",
    description="A client for the leanbase API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/leanbase/leanbase-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)