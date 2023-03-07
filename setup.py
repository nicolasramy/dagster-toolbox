from setuptools import setup, find_packages

setup(
    name="dagster-toolbox",
    version="0.0.1",
    packages=find_packages(),
    author="Nicolas RAMY",
    author_email="nicolas.ramy@darkelda.com",
    license="MIT",
    description="A set of tools to ease Dagster usage",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=[
        "dagster==1.1.5",
        "dagster-pandas==0.17.5",
        "hvac==1.0.2",
        "minio==7.1.12",
        "pandas==1.5.2",
        "python-slugify==7.0.0",
        "requests==2.28.1",
    ],
    url="https://github.com/nicolasramy/dagster-toolbox",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
        "Topic :: Terminals",
        "Topic :: Utilities",
    ],
)
