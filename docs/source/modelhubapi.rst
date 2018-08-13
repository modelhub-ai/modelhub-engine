Modelhub APIs
=============

Documentation of the Modelhub REST API and Python API


REST API
--------

The REST API is the main interface to a model packaged with the Modelhub framework.
The REST API of a running model can be called under \http::/IP_OF_MODEL:PORT/api/

TODO List and explain REST API in a nicer way. For now, please refer to the REST
API Class documentation.


REST API Class
~~~~~~~~~~~~~~
Implements the REST API

.. automodule:: modelhubapi.restapi
   :members:
   :undoc-members:
   :member-order: bysource


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
