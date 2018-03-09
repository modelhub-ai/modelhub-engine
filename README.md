| Build/Test Status | [![](https://travis-ci.org/modelhub-ai/modelhub-docker.svg?branch=master)](https://travis-ci.org/modelhub-ai/modelhub-docker) |
| --- | --- |

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
# check size ~1.7GB
docker images
# go one directory up
cd ..
# to run /data/run.py on the server (http://127.0.0.1:4000/)
docker run -p 4000:80 -v $PWD/data:/data <image_name>
# to run container in detached mode (bash)
docker run -d -p 4000:80 -v <full_path_to_your_local_data_folder>:/data <image_name> (this will return the container ID)
docker ps (check container is running and get name)
docker exec -it <container_name> bash
# kill the container
docker kill <container_name>
```

## Deployment
stay tuned!
