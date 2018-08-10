| Build/Test Status | Code Coverage | Documentation |
| :---: | :---: | :---: |
| [![](https://travis-ci.org/modelhub-ai/modelhub-engine.svg?branch=master)](https://travis-ci.org/modelhub-ai/modelhub-engine) | [![Coverage Status](https://coveralls.io/repos/github/modelhub-ai/modelhub-engine/badge.svg?branch=master&service=github)](https://coveralls.io/github/modelhub-ai/modelhub-engine?branch=master) | [![Documentation Status](https://readthedocs.org/projects/modelhub/badge/?version=latest)](https://modelhub.readthedocs.io/en/latest/?badge=latest) |


# modelhub-engine

Backend library, framework, and API for models in modelhub http://modelhub.ai/

Library and common framework on which model contributors must base their model contribution. The framework handles/provides
* data I/O
* data conversion to/from numpy (typical data format used in deep learning libraries)
* generic API for accessing and working with the model
* “slots” for preprocessing, postprocessing, and inference, which have to be populated by the contributor with the model specific code

For a detailed technical documentation of the whole Modelhub project and infrastructure see [modelhub.readthedocs.io](http://modelhub.readthedocs.io).


## Developer info

**/docker** contains files for building the specific docker images for a model.

**/docs** documentation of classes and functions of the framework.

**/framework** contains the modelhub framework code.

Template files for the contributer source (integrating the actual net plus required pre- and postprocessing) are locateded [here](https://github.com/modelhub-ai/model-template). Instructions on how to prepare a new contribution can be found [here](https://github.com/modelhub-ai/modelhub).

### Running a model with a development version of the framework
For deployment of a model the framework is part of the runtime docker. However, when developing on the framework you would not want to re-build a docker to test each change. Hence the start script [here](https://github.com/modelhub-ai/modelhub) has the option to mount a framework folder, temporarily replacing the internal framwork:
```
python start.py MODEL_NAME -mf PATH_TO_FRAMEWORK
```

## Acknowledgements

See NOTICE file in **/framework** for acknowledgements of third party technologies used.

