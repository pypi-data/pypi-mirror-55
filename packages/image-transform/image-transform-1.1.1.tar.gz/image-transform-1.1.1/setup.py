import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="image-transform",
    version="1.1.1",
    author="Mo Almishkawi",
    author_email="",
    description="Image processing and transformations",
    long_description="Image processing and transformations like scaling, \
        flipping, and cropping images",
    long_description_content_type="text/markdown",
    url="https://github.com/almishkawi/image_transform",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
