## Contribute Your Model to Modelhub

The following figure gives an overview of the necessary steps to package your model
with the Modelhub framework and eventually contributing it to the Modelhub collection.
Read further for detailed explanations of all steps.

<img width="75%" alt="modelhub contribution steps" src="https://raw.githubusercontent.com/modelhub-ai/modelhub-engine/master/docs/source/images/contribution_process.png">

**_HINT_** Take a look at an already integrated model to understand how it looks when finished ([AlexNet](https://github.com/modelhub-ai/AlexNet) is a good and simple example. If you have a more complex model with more than one input for a single inference, have a look at one of the BraTS models, e.g. [lfb-rwth](https://github.com/modelhub-ai/lfb-rwth)).

### Prerequisites

To package a model with our framework you need to have the following prerequisites installed:

- Python 2.7 or Python 3.6 (or higher)
- [Docker](https://docs.docker.com/install/)
- Clone of the [modelhub-engine repository](https://github.com/modelhub-ai/modelhub-engine.git) (`git clone https://github.com/modelhub-ai/modelhub-engine.git`)
- For GPU support, you need Docker version >= 19.03 and follow the [instructions here](https://github.com/NVIDIA/nvidia-docker#quickstart).
  <br/><br/>

### 1. Prepare Docker image

1.  Write a dockerfile preparing/installing all third party dependencies your model needs
    (e.g. the deep learning library you are using). Use the `ubuntu:16.04` Docker image as base. If you want to use CUDA and GPU acceleration, you can also use one of the `nvidia/cuda` images as base.

    You can find examples of dockerfiles for DL environments in the model repositories of
    [modelhub-ai on github](https://github.com/modelhub-ai) (e.g. for [squeezenet](https://github.com/modelhub-ai/squeezenet/blob/master/dockerfiles/caffe2)).
    <br/><br/>

2.  Build the docker image.
    <br/><br/>

3.  Adapt the [_Dockerfile_modelhub_](https://github.com/modelhub-ai/modelhub-engine/blob/master/Dockerfile_modelhub)
    located in the modelhub-engine repository to use your docker image as base
    (i.e. change the `FROM XXXXXXXX` line to `FROM <your docker image>`). No other
    changes should be necessary.
    <br/><br/>

4.  Build the image from the modified _Dockerfile_modelhub_. This will include the modelhub engine into your docker. Make sure to build it from within the modelhub-engine repository so it finds the modelhub
    framework which it will include in the Docker.
    <br/><br/>

5.  Push the image from the previous step to [DockerHub](https://hub.docker.com/)
    (required if you want to publish your model on Modelhub, so the image can
    be found when starting a model for the first time. If you don't plan to publish on Modelhub, this step is optional).

- **_NOTE_** We are planning to provide a few pre-built Docker images for the most common deep
  learning frameworks, so you do not have to build them yourself. For now we only have a small set.
  You can find the existing
  [pre-build images on DockerHub](https://hub.docker.com/u/modelhub/) - use the ones that end with '-modelhub' (the ones that don't end with '-modelhub' have only the pure DL environment without
  the modelhub framework on top.

  If the DL environment, the exact version of the DL environment, or third party dependencies
  you require are not available in the pre-build dockers, you have to build it yourself,
  following the above steps.
  <br/><br/>

### 2. Prepare your model based on the modelhub template

1.  Fork the [model template](https://github.com/modelhub-ai/model-template).
    <br/><br/>

2.  Change the name of your model-template fork to your model's name. For this open your fork on GitHub,
    go to _Settings_, change the _Repository name_, and press _Rename_.
    <br/><br/>

3.  Clone your renamed fork to your local computer and open the cloned folder.
    <br/><br/>

4.  Populate the configuration file _contrib_src/model/config.json_ with the relevant information about your model.
    Please refer to the [schema](https://github.com/modelhub-ai/modelhub/blob/master/config_schema.json) for
    allowed values and structure.
    <br/>
    Version 0.4 and up breaks the compatibility with older versions of the schema, please validate your configuration file against the current schema if you are submitting a new model. Old models are still compatible anddon't need to be changed unless you are updating the modelhub-engine version of the Docker image. For single-input models, assign the key `"single"` to your input as in the schema above. </br><br/>
    **_HINT_** For more details on how to set up your model for various input scenarios and implement your own ImageLoader class, see the [IO Configuration documentation](https://modelhub.readthedocs.io/en/latest/modelio.html).
    <br/><br/>

5.  Place your pre-trained model file(s) into the _contrib_src/model/_ folder.
    <br/><br/>

6.  (optional) Place some sample data into the _contrib_src/sample_data/_ folder. This is not mandatory
    but highly recommended, so users can try your model directly.
    <br/><br/>

7.  Open _contrib_src/inference.py_ and replace the model initialization and inference with your
    model specific code. The template example shows how to integrate models in ONNX format and running
    them in caffe2. If you are using a different model format and/or backend you have to change this.

    There are only two lines you have to modify. In the `__init__` function change the following line,
    which loads the model:

    ```python
    # load the DL model (change this if you are not using ONNX)
    self._model = onnx.load('model/model.onnx')
    ```

    If your model receives more than one file as input, the `input` argument of `infer` is a dictionary matching the input schema specified in `config.json`. You would then need to pass each individual input through the preprocessing and to your inference function. For example, accessing the input `image_pose` would look like this: `input["image_pose"]["fileurl"]`.
    <br/>
    In the `infer` function change the following line, which runs the model prediction on the input data:

    ```python
    # Run inference with caffe2 (change this if you are using a different DL framework)
    results = caffe2.python.onnx.backend.run_model(self._model, [inputAsNpArr])
    ```

    **Note** Feel free to add functions to the _Model_ class as needed to structure your model's initialization
    and execution code. But make sure to keep the pre- and post-processing of the input data and prediction
    results (done by the _ImageProcessor_) as they are. In the next step you will implement the _ImageProcessor_.
    <br/><br/>

8.  Open _contrib_src/processing.py_ to implement the _ImageProcessor_ class. The _ImageProcessor_ inherits
    from _ImageProcessorBase_, which already has most of the required data I/O processing implemented. Just your model
    specific pre- and post-processing has to be implemented, to make the _ImageProcessor_ work. There are two
    pre-processing functions and one post-processing function to be filled in. We'll go through each of these
    functions individually:

    1. **\_preprocessBeforeConversionToNumpy(self, image)**

       The _ImageProcessorBase_ takes care of loading the input image and then calls this function to let you
       perform pre-processing on the image. The image comming into this function is either a
       [PIL](https://pillow.readthedocs.io/en/latest/) or a [SimpleITK](http://www.simpleitk.org/) object.
       So _\_preprocessBeforeConversionToNumpy_ gives you the option to perform pre-processing using PIL
       or SimpleITK, which might be more convenient than performing pre-processing on the image in numpy format
       (see next step). If you decide to implement pre-porcessing here, you should implement it for both, PIL and
       SimpleITK objects. Make sure this function returns the same type of object as it received (PIL in => PIL out,
       SimpleITK in => SimpleITK out).

       You do not have to implement this. You can delete this function and implement
       all your pre-processing using the image converted to numpy (see next step).
       <br/><br/>

    2. **\_preprocessAfterConversionToNumpy(self, npArr)**

       After the image has passed through the previous function, it is automatically converted to a numpy array
       and then passed into this function. Here you must implement all additional pre-processing and numpy re-formating
       necessary for your model to perform inference on the numpy array. The numpy array returned by this function
       should have the right input format for your model (the output of this function is exactly what is returned
       by `self._imageProcessor.loadAndPreprocess(input)` in _contrib_src/inference.py_).
       <br/><br/>

    3. **computeOutput(self, inferenceResults)**

       This function receives the direct output of your model's inference. Here you must implement all
       post-processing required to prepare the output in a format that is supported by Modelhub.

       You can either output a list of dictionaries, where each dictionary has a "label" element, giving the
       name of a class, and a "probability" element, giving the probability of that class. For example:

       ```python
       result = []
       for i in range (len(inferenceResults)):
           obj = {'label': 'Class ' + str(i),
                  'probability': float(inferenceResults[i])}
           result.append(obj)
       ```

       For this you have to specifiy the output type "label*list" in your model's \_config.json*.

       Or you can output a numpy array. The output type specified in model's _config.json_ will help
       users (and Modelhub) to interpret the meaning result array:

       <table>
       <thead>
          <tr>
          <th>Name&emsp;
          <th>Description
          <th>File type
       </thead>
       <tr>
          <td>label_list&emsp;
          <td>probabilities
          <td>json
       <tr>
          <td>contour_2d&emsp;
          <td>A list (or lists) of [x,y] coordinates identifying the contour of a mask.
          <td>json
       <tr>
          <td>contour_3d&emsp;
          <td>A list (or lists) of [x,y,z] coordinates identifying the contour of a mask.
          <td>json
       <tr>   
          <td>vector&emsp;
          <td>1d
          <td>h5
       <tr>
          <td>mask_image&emsp;
          <td>2d or 3d, discrete values. 0 is always background, 1,2... are the regions
          <td>h5
       <tr>
          <td>heatmap&emsp;
          <td>2d grayscale, 2d multi, 3d grayscale, 3d multi. If normalized, 1 is highest, 0 is lowest
          <td>h5
       <tr>
          <td>image&emsp;
          <td>2d grayscale, 2d multi, 3d grayscale, 3d multi
          <td>h5            
       <tr>
          <td>custom&emsp;
          <td>none of the above
          <td>-
       </table>

9.  Edit _init/init.json_ and add the id of your Docker, so when starting your model, Modelhub knows
    which Docker to use (and download from DockerHub).

    Optionally also list any additional files that are hosted externally (i.e. not in your model's GitHub repository).
    Specify origin and the destination within your model's folder structure. This is particularly useful for
    pre-trained model files, since they can easily be larger than the maximum file size allowed in a GitHub repository.

    When starting a model, Modelhub will first download the model's repository, then download any external files,
    and then start the Docker specified in this init file.
    <br/><br/>

10. Add your licenses for the model (i.e. everything in the repsoitory except the sample data) and the license
    for the sample data to _contrib_src/license/model_ and _contrib_src/license/sample_data_ respectively.

    If you want to publish your model via Modelhub, make sure the licenses allow us to use your code, model, and
    sample data (most of the popular open source licenses should be fine, for proprietary licenses you might need
    to give Modelhub and its users explicit permission).
    <br/><br/>

11. (optional) Customize example code in _contrib_src/sandbox.ipynb_. This jupyter notebook is supposed
    to showcase how to use your model and interpret the output from python. The standard example code in this
    notebook is very basic and generic. Usually it is much more informative to a user of your model if the
    example code is tailored to your model.

    You can access and run the Sandbox notebook by starting your model via `python start.py YOUR_MODEL_FOLDER_NAME -e`.
    For this, copy _start.py_ from the [modelhub repository](https://github.com/modelhub-ai/modelhub) to the
    parent folder of your model folder.
    <br/><br/>

12. It is good practice to include the Dockerfiles your used to build the Docker for your model
    so other users can comprehend what the Docker contains. Create a folder _dockerfiles/_ in your
    local model clone (next to _contrib_src/_ and _init/_) and copy the files from steps 1.1. and
    1.3. into this folder.
    <br/><br/>

### 3. Test your model

1.  Manually check if your model works.

    1. Copy _start.py_ from the
       [modelhub repository](https://github.com/modelhub-ai/modelhub) to the parent folder of your model folder.
       <br/><br/>

    2. Run `python start.py YOUR_MODEL_FOLDER_NAME` and check if the web app for your model looks and
       works as expected. **TODO:** Add info on how to use the web app, because the command just
       starts the REST API, which the web frontend is accessing. <br/>
       **_NOTE_** If your code uses CUDA on a GPU, you have to add the `-g` flag to `start.py` to enforce the use of the GPU version of Docker. This is only required for testing, once your model is added to the index, the right mode (GPU or CPU) is automatically queried. Run `python start.py -h` for more info.
       <br/><br/>

    3. Run `python start.py YOUR_MODEL_FOLDER_NAME -e` and check if the jupyter notebook _contrib_src/sandbox.ipynb_
       works as expected.

2.  Run automatic integration test. This test will perform a few sanity checks to verify that all the basics
    seem to be working properly. However, passing this test does not mean your model performs correctly
    (hence the manual checks).

    1. Copy _test_integration.py_ from the
       [modelhub repository](https://github.com/modelhub-ai/modelhub) to the parent folder of your model folder.
       <br/><br/>

    2. Run `python test_integration.py YOUR_MODEL_FOLDER_NAME`. If all tests pass you are good to publish.

       On some platforms and Docker daemon versions communication to the model's Docker container might
       fail if the Docker is started implicitly by the integration test. If you get obscure errors
       during test, try starting your model idependently in a different terminal via `python start.py YOUR_MODEL_FOLDER_NAME` and running the test with the "-m" option: `python test_integration.py YOUR_MODEL_FOLDER_NAME -m`.

       If your model needs particularly long to start up, you need to tell the integration test how long
       to wait before attempting to communicate with the model. Use the "-t" option.

       Check out the documentation of the integration test by calling `python test_integration.py -h`
       <br/><br/>

### 4. Publish

1.  `git clone https://github.com/modelhub-ai/modelhub.git` (or update if you cloned already).
    <br/><br/>

2.  Add your model to the model index list _models.json_. If your model needs a GPU to run, add `"gpu" : true` to the parameters for your model. This tells the start script to run the model with GPU acceleration.
    <br/><br/>

3.  Send us a pull request.
    <br/><br/>
