from setuptools import setup, find_packages

with open("README.md","r") as readme_file:
    readme = readme_file.read()

requirements = ["pandas>=0.24","tqdm>=4","SQLAlchemy>=1.3"]

setup(
    name="bulketl",
    version="0.0.1",
    author="Pete Griffin",
    author_email="peteyg543@gmail.com",
    description="A package for loading files to data warehouse in bulk",
    long_description=readme,
    long_description_content_type="text/markdown",
    url='https://github.com/griffinpf/bulketl',
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ]
)