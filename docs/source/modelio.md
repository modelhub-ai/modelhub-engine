## Modelhub IO Configuration

### Input Configuration for Single Inputs

#### As a User
If the model only requires a single image or other type of file for inference, you can simply pass a URL or a path to a local file to the API. For example, you can detect objects using YOLO-v3 by running `python start.py yolo-v3` and then use the API like this:
```
http://localhost:80/api/predict?fileurl=http://example.org/cutedogsandcats.jpg
```
The API then returns the prediction in the specified format.

#### As a Collaborator submitting a new Model
For single inputs, please create a configuration for your model according to the [example configuration](https://github.com/modelhub-ai/modelhub/blob/master/example_config_single_input.json). It is important that you keep the key `"single"` in the config, as the API uses this for accessing the dimension constraints when loading an image. Populate the rest of the configuration file as stated in the contribution guide and the [schema](https://github.com/modelhub-ai/modelhub/blob/master/config_schema.json). Validate your config file against our config schema with a JSON validator, e.g. [this one](https://www.jsonschemavalidator.net).<br/>
Take care to choose the right MIME type for your input, this format will be checked by the API when users call the predict function and load a file. We support a few extra MIME types in addition to the standard MIME types:
<table>
<thead>
  <tr>
  <th> MIME type&emsp;
  <th> File extension&emsp;
  <th> Description&emsp;
</thead>
<tr>
  <td> "application/nii"&emsp;
  <td> .nii&emsp;
  <td> Nifti-1 image&emsp;
<tr>
  <td> "application/nii-gzip"&emsp;
  <td> .nii.gz&emsp;
  <td> Compressed Nifti-1 image&emsp;
<tr>
  <td> "application/nrrd"&emsp;
  <td> .nrrd&emsp;
  <td> NRRD image&emsp;
</table>


<br/><br/>
If you need other types not supported in the standard MIME types and by our extension, please open an [issue on Github](https://github.com/modelhub-ai/modelhub/issues).
<br/><br/>

### Input Configuration for Multiple Inputs

#### As a User
When you use a model that needs more than a single input file for a prediction, you have to pass a JSON file with all the inputs needed for that model. You can have a look at an example [here](https://github.com/modelhub-ai/modelhub/blob/master/example_input_file_multiple_inputs.json). <br/>
The important points to keep in mind are:
- There has to be a `format` key with `"application/json"` so that the API can handle the file
- Each of the other keys describes one input and has to have a `format` (see the MIME types above) and a `fileurl`

<br/><br/>
The `fileurl` can contain a path to a local file (which has to be accessible by the Docker container running the model) or can contain a URL to a file on the web. The REST API can handle both and a mixture of local and web links while the Python API can only access local paths. <br/>
Passing an input file to the REST API would then look like this:
```
http://localhost:80/api/predict?fileurl=http://example.org/fourimagesofdogs.json
```
<br/><br/>
#### As a Collaborator submitting a new Model
For multiple inputs, please create a configuration for your model according to the [example configuration](https://github.com/modelhub-ai/modelhub/blob/master/example_config_multiple_inputs.json). The `format` key has to be present at the `input` level and must be equal to `application/json` as all input files will be passed in a json to the API.
<br/>
The other keys stand for one input file each and must contain a valid format (e.g. `application/dicom`) and dimensions. You can additionally add a description for the input.
<br/>
Populate the rest of the configuration file as stated in the contribution guide and the [schema](https://github.com/modelhub-ai/modelhub/blob/master/config_schema.json). Validate your config file against our config schema with a JSON validator, e.g. [this one](https://www.jsonschemavalidator.net).<br/><br/>
To access the files passed to your model in the `infer` function, use the keys you specified in the configuration and in the input json file. For example, suppose you have an input with key `t1`: You can access the path the the file in `infer` by using the passed dictionary: `input["t1"]["fileurl"]`. This way you can always be sure that you are accessing the right file. <br/><br/>
**_HINT_** You can implement additional classes for the loading of your images by adding your own class that extends the `ImageLoader` class and add it to the chain of responsibility for loading the images. One good example is the [lfb-rwth](https://github.com/modelhub-ai/lfb-rwth) model.
<br/><br/>
Additionally, mismatches between the config file and the input file the user passes to the API are automatically checked before the input is passed to your model.
<br/><br/>
**_HINT_** Check out existing models with multiple inputs to see how they implemented the input handling of multiple inputs, for example one of the BraTS models, e.g. [lfb-rwth](https://github.com/modelhub-ai/lfb-rwth).
