import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="modelhub-ai",
    version="0.0.4",
    author="modelhub",
    author_email="info@modelhub.ai",
    description="Crowdsourced through contributions by the research community, modelhub.ai is a repository of deep learning models for various data types.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/modelhub-ai",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
