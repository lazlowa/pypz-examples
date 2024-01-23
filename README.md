# Build artifacts

1. Python build required (https://github.com/pypa/build).
```shell
python -m pip install build
```
2. Adapt the pyprject.toml file according to your spec
3. Build the project
```shell
python -m build
```

# Build Docker image
Once the artifacts have been built and are present in the ./dist folder
you can build the Docker image. Note that choosing the image tag is your
responsibility. It shall reflect the image repository onto which you
want to deploy the image. Should you use Kubernetes, the image repository
shall be accessible by the cluster.
```shell
docker build -t accessible-repository/pypz-example .
```