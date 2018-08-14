This folder contains the Modelhub documentation files. We are using Sphinx to build our documentation and include code documentation. The Modelhub documentation is hosted at [modelhub.readthedocs.io](http://modelhub.readthedocs.io). _Read the Docs_ builds the documentation automatically. Nevertheless, if you want to build the docs locally, [see below](#how-to-build-the-docs-locally).

### Read The Docs Admin Page for Modelhub
https://readthedocs.org/projects/modelhub/

### How to build the docs locally

#### Prerequisites
```
pip install Sphinx
pip install sphinx_rtd_theme
pip install recommonmark
```

#### Build
Open a terminal and navigate to this folder (_modelhub-engine/docs_) in your local clone of this repository. Then execute:
```
make html
```
The documentation will be generated into the subfolder _build_
