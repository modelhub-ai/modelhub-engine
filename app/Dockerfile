# Use our Caffe2 base image as parent
FROM modelhub/base_caffe2:1.0.0

# Install requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80 81

# Define environment variable
ENV PYTHONPATH /usr/local:/framework/:/contrib_src/

# Netron fixes
# change header line in netron
RUN sed -i '1s:.*:#!/usr/bin/python:' /usr/local/bin/netron
# copy bugfix sources, fixing netron hanging on multiple requests
# this should not be necessary anymore when netron > 1.7.4 is available (which should contain the fix)
WORKDIR /usr/local/lib/python2.7/dist-packages/netron
RUN curl -O https://raw.githubusercontent.com/lutzroeder/Netron/9ad8d0ea9bd67f306f8d3bc5559859cf37517534/src/netron
RUN curl -O https://raw.githubusercontent.com/lutzroeder/Netron/9ad8d0ea9bd67f306f8d3bc5559859cf37517534/src/netron.py
RUN curl -O https://raw.githubusercontent.com/lutzroeder/Netron/9ad8d0ea9bd67f306f8d3bc5559859cf37517534/src/onnx-operator.json

# Set the working directory to /framework
WORKDIR /framework

# Copy the framework directory contents into the container at /framework
ADD /framework /framework

# Create dir where uploads go (e.g. from the webservice)
WORKDIR /uploads

# Switch to the dir that holds the usr sources
WORKDIR /contrib_src

# Run /data/run.py when the container launches
CMD ["python", "run.py"]
