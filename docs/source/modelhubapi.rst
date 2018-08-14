Modelhub APIs
=============

Documentation of the Modelhub REST API and Python API


REST API
--------

The REST API is the main interface to a model packaged with the Modelhub framework.
The REST API of a running model can be reached under \http://<ip of model>:<port>/api/<call>.
For example :code:`http://localhost:80/api/get_config` to retrieve a JSON string with the model
configuration

See the following documentation of the REST API Class for a documentation of 
all available functions.


REST API Class
~~~~~~~~~~~~~~
Implements the REST API

.. automodule:: modelhubapi.restapi
   :members:
   :undoc-members:
   :member-order: bysource
   :exclude-members: start

Python API
----------

The Python API is a convenience interface to a model when you have direct access to
the modelhub runtime environment, i.e. when you are inside the Docker running the model.
This is for example the case if you work with the sandbox Jupyter notebook provided 
with the model you are running.


Python API Class
~~~~~~~~~~~~~~~~
Implements the Python API

.. automodule:: modelhubapi.pythonapi
   :members:
   :undoc-members:
   :member-order: bysource
