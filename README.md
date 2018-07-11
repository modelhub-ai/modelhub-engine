| Build/Test Status | Code Coverage |
| :---: | :---: |
| [![](https://travis-ci.org/modelhub-ai/modelhub-engine.svg?branch=master)](https://travis-ci.org/modelhub-ai/modelhub-engine) | [![Coverage Status](https://coveralls.io/repos/github/modelhub-ai/modelhub-engine/badge.svg?branch=master&service=github)](https://coveralls.io/github/modelhub-ai/modelhub-engine?branch=master) |


# modelhub-engine

Backend framework for running models in modelhub.

## Development

**/app** contains files for building the docker image.

**/framework** contains the modelhub framework providing a convenient backend to run inference on DL models incl. pre- and postprocessing, and a frontend for basic + expert access to the model.

**/usr_src_template** template files for the user/contributer source which provides the full model (i.e. the actual net plus required pre- and postprocessing). Note that actual user/contributer sources (i.e. full models) are [located in a different repository.](https://github.com/modelhub-ai/modelhub)

```
# clone this repo
git clone https://github.com/modelhub-ai/modelhub-engine.git
# change directories
cd modelhub-engine/app/
# build docker image from /app folder
docker build -f Dockerfile.dev -t <name_your_image> .
# check size ~1.5GB
docker images
# go one directory up
cd ..
# to run /contrib_src/run.py on the server (http://127.0.0.1:4000/)
# and mount the framwork and user code into the docker
docker run -p 4000:80 -v $PWD/framework:/framework -v $PWD/contrib_src:/contrib_src <image_name>
# to get a bash in an interactive mode of the docker
docker run -it -p 4000:80 -v $PWD/framework:/framework -v $PWD/usr_src:/usr_src <image_name> /bin/bash
# to run container in detached mode (bash)
docker run -d -p 4000:80 -v $PWD/framework:/framework -v $PWD/usr_src:/usr_src <image_name> (this will return the container ID)
docker ps (check container is running and get name)
docker exec -it <container_name> bash
# kill the container
docker kill <container_name>
```

## Deployment

stay tuned!

## Acknowledgements

see notice.md file in this repository for acknowledgements of third party technologies used

