## How to build the Docker images

Execute the docker build command **from the parent directory** of this one,
with the following command:

```
docker build -t <name+tag> -f docker/<docker-file-name> .
```

## How to push an image to DockerHub

Make sure the Docker name starts with "modelhub/" and the tag should also be
a unique version number (e.g. "modelhub/release:1.2.3").

Then login to docker with your credentials:
```
docker login
```

Upload the docker you created:
```
docker push <name+tag>
```

Logout:
```
docker logout
```
