## Quick Start

The most accessible way to experience modelhub is via [modelhub.ai](http://www.modelhub.ai). There you can explore the model collection, try them online, and find instructions on how to run models locally.

But since you are here, follow these steps to get modelhub running on your local computer:

1. **Install Docker** (if not already installed)

   Follow the [official Docker instructions](https://docs.docker.com/install/) to install Docker CE.
   Docker is required to run models.<br/>
   **GPU Support**: If you want to run models that require GPU acceleration, please use Docker version >= 19.03 and follow the installation instructions for the [Nvidia-Docker Toolkit here](https://github.com/NVIDIA/nvidia-docker#quickstart).
   <br/><br/>

2. **Install Python 2.7 or 3.6 (or higher)** (if not already installed)

   Download and install Python from the [official Python page](https://www.python.org/). Modelhub requires
   Python 2.7 or Python 3.6 (or higher).
   <br/><br/>

3. **Install the modelhub-ai package**

   Install the `modelhub-ai` package from PyPi using pip: `pip install modelhub-ai`.  
   <br/><br/>

4. **Run a model using start.py**

   Open a terminal and navigate to a folder you want to work in. For running models, write access
   is required in the current folder.

   Execute `modelhub-run squeezenet` in the terminal to run the squeezenet model from the modelhub collection.
   This will download all required model files (only if they do not exist yet) and start the model. Follow the
   instructions given on the terminal to access the web interface to explore the model.

   Replace `squeezenet` by any other model name in the collection to start a different model. To see a list of
   all available models execute `modelhub-list` or `modelhub -l`.

   You can also access a jupyter notebook that allows you to experiment with a model by starting a model with
   the "-e" option, e.g. `modelhub-run squeezenet -e`. Follow the instructions on the terminal to open the notebook.

   See additional starting options by executing `modelhub-run -h`.
   <br/><br/>
