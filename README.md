| Build/Test Status | [![](https://travis-ci.org/modelhub-ai/modelhub-docker.svg?branch=master)](https://travis-ci.org/modelhub-ai/modelhub-docker) |
| ----------------- | ----------------------------------------------------------------------------------------------------------------------------- |


| Docker Status | [![](https://images.microbadger.com/badges/image/modelhub/onnx-docker.svg)](https://microbadger.com/images/modelhub/onnx-docker "Get your own image badge on microbadger.com") |
[![](https://images.microbadger.com/badges/version/modelhub/onnx-docker.svg)](https://microbadger.com/images/modelhub/onnx-docker "Get your own version badge on microbadger.com") |
| --- | --- | --- |

# modelhub-docker

Files for creating a base modelhub docker image

## Development

**/app** contains files for building the docker image.

**/framework** contains the modelhub framework providing a convenient backend to run inference on DL models incl. pre- and postprocessing, and a frontend for basic + expert access to the model.

**/usr_src_template** template files for the user/contributer source which provides the full model (i.e. the actual net plus required pre- and postprocessing). Note that actual user/contributer sources (i.e. full models) are [located in a different repository.](https://github.com/modelhub-ai/modelhub)

```
# clone this repo
git clone https://github.com/modelhub-ai/modelhub-docker.git
# change directories
cd modelhub-docker/app/
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
