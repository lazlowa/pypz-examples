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
from pypz.deployers.k8s import KubernetesDeployer

from pypz.example.pipeline import DemoPipeline

"""
This example shows, how to create a pipeline object and how to deploy it 
onto a Kubernetes cluster with the KubernetesDeployer.
"""

if __name__ == "__main__":
    """ Notice that unlike in the case of plugins and operators, the "name" ctor argument
        is defined here. The reason is that to use the variables' name as instance name,
        we need to control the context, where the variable is set. This is the case for
        plugins and operators, but not for pipelines, hence it is required to provide
        an instance name for pipelines."""
    pipeline = DemoPipeline("pipeline")

    """ Since this example uses kafka ports, the parameter "channelLocation" shall be set
        tp a valid Kafka broker's URL. """
    pipeline.set_parameter(">>channelLocation", "KAFKA_BROKER_URL")

    """ Sets the required parameter of the DemoWriterOperator """
    pipeline.writer.set_parameter("recordCount", 30)

    """ The KubernetesDeployer is an implementation of the Deployer interface, which
        allows the deployment of entire pipelines on Kubernetes. For each operator a
        Pod will be created and executed. The pipeline configuration is stored as
        secret. """
    deployer = KubernetesDeployer(namespace="NAMESPACE")

    """ Deploy only, if it is not yet deployed """
    if not deployer.is_deployed(pipeline.get_full_name()):
        deployer.deploy(pipeline)

    """ Attach to the deployed pipeline, which blocks the execution until the
        pipeline is finished i.e., all operators are finished in the pipeline. """
    deployer.attach(pipeline.get_full_name())

    """ Destroy all pipeline related resources on Kubernetes """
    deployer.destroy(pipeline.get_full_name())
