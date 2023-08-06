import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name='ColorHelper',
    version='0.1',
    author="Subin An",
    author_email="subinium@gmail.com",
    description="ML based Color Palette Generator Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/subinium/ColorHelper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
    ],
)
