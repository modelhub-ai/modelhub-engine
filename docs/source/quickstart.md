## Quick Start

The most accessible way to experience modelhub is via [modelhub.ai](http://www.modelhub.ai). There you can explore the model collection, try them online, and find instructions on how to run models locally.

But since you are here, follow these steps to get modelhub running on your local computer:

1. **Install Docker** (if not already installed)

   Follow the [official Docker instructions](https://docs.docker.com/install/) to install Docker CE.
   Docker is required to run models.
   <br/><br/>

2. **Install Python 2.7 or 3.6 (or higher)** (if not already installed)

   Download and install Python from the [official Python page](https://www.python.org/). Modelhub requires
   Python 2.7 or Python 3.6 (or higher).
   <br/><br/>

3. **Download modelhub start script**

   Download [_start.py_](https://raw.githubusercontent.com/modelhub-ai/modelhub/master/start.py)
   (right click -> "save link as") from the [modelhub repository](https://github.com/modelhub-ai/modelhub) and place it into an empty folder.
   <br/><br/>

4. **Run a model using start.py**

   Open a terminal and navigate to the folder that contains _start.py_. For running models, write access
   is required in the current folder.

   Execute `python start.py squeezenet` in the terminal to run the squeezenet model from the modelhub collection.
   This will download all required model files (only if they do not exist yet) and start the model. Follow the
   instructions given on the terminal to access the web interface to explore the model.

   Replace `squeezenet` by any other model name in the collection to start a different model. To see a list of
   all available models execute `python start.py -l`.

   You can also access a jupyter notebook that allows you to experiment with a model by starting a model with
   the "-e" option, e.g. `python start.py squeezenet -e`. Follow the instructions on the terminal to open the notebook.

   See additional starting options by executing `python start.py -h`.
   <br/><br/>
