import setuptools

from PyJsonFriendly._version import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyJsonFriendly",
    version=__version__,
    author="Mohammad Abouali",
    author_email="maboualidev@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maboualidev/PyJsonFriendly",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7'
)