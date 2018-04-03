#!/bin/bash

declare -r dockerIdentifier="modelhub/test:1.1"
declare -r serverAddress="https://raw.githubusercontent.com/modelhub-ai/modelhub-docker/master/"
declare -r modelIdentifier="usr_src"
declare -a -r requiredFiles=("$modelIdentifier""/inference.py"
                             "$modelIdentifier""/postprocessing.py"
                             "$modelIdentifier""/preprocessing.py"
                             "$modelIdentifier""/run.py"
                             "$modelIdentifier""/sandbox.ipynb"
                             "$modelIdentifier""/model/config.json"
                             "$modelIdentifier""/model/labels.json"
                             "$modelIdentifier""/model/squeezenet.onnx"
                             "$modelIdentifier""/model/figures/thumbnail.jpg"
                            )

# ---------------------------------------------------------
# Check prerequisites
# ---------------------------------------------------------

# checking if Docker exists
if ! command -v docker >/dev/null 2>&1; then
    echo >&2 "Docker is required to run models from modelhub. Please go to https://docs.docker.com/install/ and follow the instructions to install Docker on your system."
    exit 1
fi

# get the required modelhub Docker image
echo "Getting modelhub Docker image for $modelIdentifier"
docker pull "$dockerIdentifier"

# check if model data already exists
modelFolderExists=true
if ! [ -d "$modelIdentifier" ]; then
    modelFolderExists=false
fi

# try to download data if model folder does not exist
if [ "$modelFolderExists" = false ]; then
    # trying to get model data with curl
    echo "$modelIdentifier model data folder does not exist yet."
    if command -v curl >/dev/null 2>&1; then
        echo "Getting model data with curl"
        for file in "${requiredFiles[@]}"
        do
          mkdir -p $(dirname "$file")
          curl "$serverAddress""$file" --output "$file"
        done
    elif command -v wget >/dev/null 2>&1; then
        echo "Getting model data with wget"
        for file in "${requiredFiles[@]}"
        do
          mkdir -p $(dirname "$file")
          wget -O "$file" "$serverAddress""$file"
        done
    else
        echo >&2 "cURL or Wget are required to download the model data from modelhub. Please install either of them and run this script again."
        exit 1
    fi
    echo "Done getting model data."
else
    echo "Existing model data found."
fi


# ---------------------------------------------------------
# Run model
# ---------------------------------------------------------
echo "Starting model."
docker run -p 4000:80 -v $PWD/usr_src:/usr_src "$dockerIdentifier"
