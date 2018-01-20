"""Setup script to install Neural Namer scripts."""

from setuptools import setup, find_packages

setup(
    name="neural-namer",
    version=0.1,
    description="Deep learning for fantasy names",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "crawl=crawler.commands:main",
            "preprocess=preprocessor.commands:main",
            "model=modeler.commands:main",
            "cache=web.cache.commands:main",
        ]
    }
)