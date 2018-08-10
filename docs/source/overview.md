## Overview

Modelhub provides a framework into which contributors can plug-in their model and model specific code pre- and post-processing code. The framework provides a standalone runtime environment, convience functionality (e.g. image loading and conversion), programming interfaces to access the model, and a user friendly web-interface to try a model. See the following figure for an overview of the architecture.

<img width="500" alt="modelhub framework overview" src="https://raw.githubusercontent.com/modelhub-ai/modelhub/master/docs/images/framework_overview.png">

The _contrib_src_ contains the model specific code and data, all other functionality is provided by the framework. The framework and model specific code run inside of a Docker container, which contains all runtime dependencies. The resulting package constitutes a standalone unit that can be easily deployed, executed on different platforms (Linux, Windows, Mac), and integrated into existing applications via the generic API.
