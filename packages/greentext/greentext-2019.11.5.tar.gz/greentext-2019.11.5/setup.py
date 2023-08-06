from distutils.core import setup

from setuptools import find_packages

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

setup(
    name="greentext",
    version="2019.11.05",
    description="A 4chan object library for navigating the 4chan API intuitively",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["4chan", "chan", "boards", "4chan.org", "4channel.org", "4cdn.org"],
    author="Star City Industries",
    author_email="pypi@starcity.su",
    url="https://github.com/StarCityIndustries/greentext",
    download_url="https://github.com/StarCityIndustries/greentext/archive/0.1.tar.gz",
    classifiers=["Development Status :: 1 - Planning",
                 "Programming Language :: Python :: 3",
                 "License :: OSI Approved :: MIT License",
                 "Operating System :: OS Independent",
                 "Natural Language :: English",
                 "Typing :: Typed"],
    packages=find_packages(),
    requires=["requests"],
    python_requires=">=3.6"
)
