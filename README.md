# Description
This project contains some usage examples for pypz. This project does not
intend to explain the core concepts of pypz, but just to give a starting
point to understand the basic usage. The core concepts will be documented
in the pypz repository.

# Requirements
For this example you will need the following:
- an IDE of your choice, however the project used PyCharm
- access to a Kafka cluster, since the operators are using Kafka based IO ports

## Optional
Optional, because you can create run the pipelines without the following:
- access to a Docker image repository
- access to a Kubernetes Cluster

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

# Docker image
## Build
Once the artifacts have been built and are present in the ./dist folder
you can build the Docker image. Note that choosing the image tag is your
responsibility. It shall reflect the image repository onto which you
want to deploy the image. Should you use Kubernetes, the image repository
shall be accessible by the cluster.
```shell
docker build -t accessible-repository/pypz-example .
```

### [Errno: -2] Name or service not known
Should you face this error during the image build, it probably means that
you have invalid proxy/dns settings. If you are behind a corporate proxy,
then you need to make sure that the Docker Engine is configured properly.

First, you need to locate the config file, which is usually the ~/.docker/config.json
file. Open it and insert the following setting in the json:
```json

"proxies": {
  "default": {
    "httpProxy": "<YOUR_HTTP_PROXY>",
    "httpsProxy": "<YOUR_HTTPS_PROXY>",
    "noProxy": "<YOUR_NO_PROXY>"
  }
}
```
## Push
Once the image is built, you can push it to your repository.
```shell
docker push accessible-repository/pypz-example
```
# Deploy onto Kubernetes
If you have access to a Kubernetes cluster, then you can try to deploy
the pipeline on it. The file "deploy.py" shows a small example for how
to do it. You will need the kube config file, which you can extract from
your cluster based on its control plane. If you have kubectl installed
and used, then you don't have to do anything, since the pypz K8s deployer
uses by default the same file.

Note that depending on your cluster, you might need to update your
trusted certificates. The pypz Kubernetes deployer uses "certifi", hence
if you want to locate the cacert file, you can do it via the following command:
```shell
python -c "import certifi; print(certifi.where())"
```
Then you can update this cacert file with the certificates of your cluster.

## Advanced Kubernetes parameters
If you deploy your pipeline onto Kubernetes, then you might have 
the use-case, where you need additional configuration to use existing 
kubernetes resources or mount locations into your operator etc.
One use-case is to create a secret with some credentials and reference 
it from your operator so you don't need to store sensitive information in code.
In order to specify additional kubernetes related configuration, 
the KubernetesParameter class can be used:
```python
def __init__(self,...):
    self.env: Optional[list[dict]] = env
    self.envFrom: Optional[list[dict]] = envFrom
    self.volumeMounts: Optional[list[dict]] = volumeMounts
    self.containers: Optional[list[dict]] = containers
    self.volumes: Optional[list[dict]] = volumes
    self.terminationGracePeriodSeconds: Optional[int] = terminationGracePeriodSeconds
    self.serviceAccountName: Optional[str] = serviceAccountName
    self.labels: Optional[dict] = labels
    self.containerSecurityContext: Optional[dict] = containerSecurityContext
    self.podSecurityContext: Optional[dict] = podSecurityContext
    self.nodeAffinity: Optional[dict] = nodeAffinity
    self.nodeAntiAffinity: Optional[dict] = nodeAntiAffinity
```
Check the file "deploy_with_k8s_secret.py" for an example.
