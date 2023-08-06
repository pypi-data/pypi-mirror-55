import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lookml",
    version="0.0.5",
    author="Russell Garner and Hugo Selbie",
    author_email="russelljgarner@gmail.com, hselbie@gmail.com",
    description="A pythonic api for programatically manipulating LookML",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/llooker/lookml",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
