Modelhub APIs
=============

Documentation of the Modelhub REST API and Python API


REST API
--------

The REST API is the main interface to a model packaged with the Modelhub framework.
The REST API of a running model can be reached under \http://<ip of model>:<port>/api/<call>.
For example :code:`http://localhost:80/api/get_config` to retrieve a JSON string with the model
configuration. 

The REST API is automatically instantiated when you start a model via 
:code:`python start.py <your model name>`. See the following documentation 
of the :class:`~modelhubapi.restapi.ModelHubRESTAPI` 
class for a documentation of all available functions.


REST API Class
~~~~~~~~~~~~~~

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

When you are working inside the Docker running a model, you can import the Modelhub 
Python API via :code:`from modelapi import model`. This is a convenience import,
which implicitly takes care of initializing the :class:`~modelhubapi.pythonapi.ModelHubAPI`
with the model in the current Docker. You would then call the API 
(e.g. to get the model config) like this :code:`configuration = model.get_config()`.


Python API Class
~~~~~~~~~~~~~~~~

.. automodule:: modelhubapi.pythonapi
   :members:
   :undoc-members:
   :member-order: bysource
