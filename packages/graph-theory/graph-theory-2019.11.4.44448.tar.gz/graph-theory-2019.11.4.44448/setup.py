"""
graph-theory
"""
build_tag = "f2fe38096501ccfefcb811695c9da8503c53d5aba81c6e706433189baf3ed953"
from setuptools import setup
from pathlib import Path


folder = Path(__file__).parent
file = "README.md"
readme = folder / file
assert isinstance(readme, Path)
assert readme.exists(), readme
with open(str(readme), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name="graph-theory",
    version="2019.11.4.44448",
    url="https://github.com/root-11/graph-theory",
    license="MIT",
    author="Bjorn Madsen",
    author_email="bjorn.madsen@operationsresearchgroup.com",
    description="A graph library",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords="graph graphs optimization tsp shortest-path",
    packages=["graph", "examples.optimization"],
    include_package_data=True,
    data_files=[(".", ["LICENSE", "README.md"])],
    platforms="any",
    install_requires=[],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
    ],
)


