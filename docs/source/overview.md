## Overview

### Framework

Modelhub provides a framework into which contributors can plug-in their model, and model specific pre- and post-processing code. The framework provides a standalone runtime environment, convience functionality (e.g. image loading and conversion), programming interfaces to access the model, and a user friendly web-interface to try a model. See the following figure for an overview of the architecture.

<img width="75%" alt="modelhub framework overview" src="https://raw.githubusercontent.com/modelhub-ai/modelhub-engine/master/docs/source/images/framework_overview.png">

The _contrib_src_ contains the model specific code and data, all other functionality is provided by the framework. The framework and model specific code run inside of a Docker container, which contains all runtime dependencies. The resulting package constitutes a standalone unit that can be easily deployed, executed on different platforms (Linux, Windows, Mac), and integrated into existing applications via the generic API.

### Repository Structure

The whole modelhub infrastructure is a combination of several repositories under [https://github.com/modelhub-ai](https://github.com/modelhub-ai), comprising the following:

- **modelhub** Index/Registry of all models

    Contains 
    - a list (index/registry) of all models available via modelhub
    - json schema for validating model config files
    - python script to conveniently start any model which is registered in the modelhub index
    <br/><br/>

- **modelhub-app** Generic web frontend for a model

    Web app for easy interaction with a model provides
    - relevant info about model (architecture, I/O, purpose)
    - info about accompanying publication (optional)
    - GUI interface to run/test the model

    The web app is generic and works on top of every model without modifications.
    <br/><br/>

- **modelhub-engine** Backend library, framework, and API

    Library and common framework on which model contributors must base their model contribution. The framework handles/provides
    -data I/O
    -data conversion to/from numpy (typical data format used in deep learning libraries)
    -generic API for accessing and working with the model
    -“slots” for preprocessing, postprocessing, and inference, which have to be populated by the contributor with the model specific code
    <br/><br/>

- **model-template** Template structure for building modelhub compatible models

    Defines the file and directory structure required to build a model that can be integrated into modelhub. Contributors should clone this repository and build fill in the template with their model specific code/info.
    <br/><br/>

- **\<model name\>** A model implementation available via modelhub

    Several models are directly hosted under modelhub.ai. Each model has its own repository. The structure of the repository follows the model-template. However, models don’t need to be hosted under modelhub.ai but can be any github repository. To be integrated in and available via modelhub, they only have to be listed in the modelhub index/registry.
    <br/><br/>

- **modelhub-ai.github.io** Modelhub webpage

    Source code for the [modelhub.ai webpage](http://modelhub.ai/)
    <br/><br/>

