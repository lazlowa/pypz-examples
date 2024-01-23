# =============================================================================
# Copyright (c) 2024 by Laszlo Anka. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================
from pypz.deployers.k8s import KubernetesDeployer, KubernetesParameter

from pypz.example.pipeline import DemoPipeline

if __name__ == "__main__":
    pipeline = DemoPipeline("pipeline")
    """ Notice that unlike in the case of plugins and operators, the "name" ctor argument
        is defined here. The reason is that to use the variables' name as instance name,
        we need to control the context, where the variable is set. This is the case for
        plugins and operators, but not for pipelines, hence it is required to provide
        an instance name for pipelines."""
    pipeline.set_parameter(">>channelLocation", "KAFKA_BROKER_URL")
    """ Since this example uses kafka ports, the parameter "channelLocation" shall be set
        tp a valid Kafka broker's URL. """

    deployer = KubernetesDeployer(namespace="NAMESPACE")
    """ The KubernetesDeployer is an implementation of the Deployer interface, which
        allows the deployment of entire pipelines on Kubernetes. For each operator a
        Pod will be created and executed. The pipeline configuration is stored as
        secret. """

    k8s_param = KubernetesParameter()
    secret = {
        "name": "SECRET_USERNAME",
        "valueFrom": {
            "secretKeyRef": {
                "name": "backend-user",
                "key": "backend-username"
            }
        }
    }
    """
    Defines a secret artifact just like in the Kubernetes specification.
    https://kubernetes.io/docs/tasks/inject-data-application/distribute-credentials-secure/#define-container-environment-variables-using-secret-data
    """
    k8s_param.env = [secret]

    pipeline.writer.set_parameter("kubernetes", k8s_param.__dict__)
    """
    Sets the reserved "kubernetes" parameter. Notice that we provide the "dictified" version
    of the object, since the types of the parameters are restricted to yaml tolerated
    serializable types.
    """

    pipeline.writer.set_parameter("userName", "$(env:SECRET_USERNAME)")
    """
    Sets the parameter as "runtime" template to the secret name. Runtime template means that
    it will be resolved in runtime at before execution.
    """

    if not deployer.is_deployed(pipeline.get_full_name()):
        deployer.deploy(pipeline)

    deployer.attach(pipeline.get_full_name())
    deployer.destroy(pipeline.get_full_name())
