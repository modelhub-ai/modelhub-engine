| Build/Test Status | [![](https://travis-ci.org/modelhub-ai/modelhub-docker.svg?branch=master)](https://travis-ci.org/modelhub-ai/modelhub-docker) |
| ----------------- | ----------------------------------------------------------------------------------------------------------------------------- |


| Docker Status | [![](https://images.microbadger.com/badges/image/modelhub/onnx-docker.svg)](https://microbadger.com/images/modelhub/onnx-docker "Get your own image badge on microbadger.com") |
[![](https://images.microbadger.com/badges/version/modelhub/onnx-docker.svg)](https://microbadger.com/images/modelhub/onnx-docker "Get your own version badge on microbadger.com") |
| --- | --- | --- |

# modelhub-docker

Files for creating a base modelhub docker image

## Development

**/app** contains files for building the docker image.

**/data** contains files that will be mount as a volume to the docker container. This way, dev ops can continue on files under /data without having to rebuild the image every time. /data will not persist in the docker when it is killed, but we have it locally and in this repo.

```
# clone this repo
git clone https://github.com/modelhub-ai/modelhub-docker.git
# change directories
cd modelhub-docker/app/
# build docker image from /app folder
docker build -t <name_your_image> .
# check size ~1.5GB
docker images
# go one directory up
cd ..
# to run /usr_src/run.py on the server (http://127.0.0.1:4000/)
# and mount the framwork and user code into the docker
docker run -p 4000:80 -v $PWD/framework:/framework -v $PWD/usr_src:/usr_src <image_name>
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
