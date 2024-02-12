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
import sys
import traceback
from datetime import datetime

from pypz.core.specs.operator import Operator
from pypz.deployers.base import DeploymentState
from pypz.deployers.k8s import KubernetesDeployer

from pypz.example.pipeline import DemoPipeline

"""
This example shows, how to create a pipeline object and how to deploy it 
onto a Kubernetes cluster with the KubernetesDeployer. In addition, it shows,
how to monitor your pipeline and perform actions in error state, like
write the logs into file and restart the operator.
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

    """ Expect to raise an error after 5 records received by the reader operator """
    pipeline.reader.set_parameter("raiseErrorAfterRecordCount", 5)

    """ The KubernetesDeployer is an implementation of the Deployer interface, which
        allows the deployment of entire pipelines on Kubernetes. For each operator a
        Pod will be created and executed. The pipeline configuration is stored as
        secret. """
    deployer = KubernetesDeployer(namespace="NAMESPACE")

    """ Deploy only, if it is not yet deployed """
    if not deployer.is_deployed(pipeline.get_full_name()):
        deployer.deploy(pipeline)

    def state_monitor(operator: Operator, state: DeploymentState) -> None:
        """
        This method will be called for every state change for every
        operator in the pipeline. In case of operator error, it will
        persist the logs and attempts to restart the operator.
        """

        if DeploymentState.Failed == state:
            try:
                print("Error")
                logs = deployer.retrieve_operator_logs(operator.get_full_name())

                """ Name of the log file is set to the operator name and the current datetime """
                with open(operator.get_full_name() + "_" + datetime.now().strftime("%Y%m%d_%H%M%S"), "w") as f:
                    f.write(logs)
            except:
                """ Do nothing, just print exception, hence the operator can be restarted 
                    even, if there is an error in log retrieval or persistence"""
                traceback.print_exc(file=sys.stderr)

            deployer.restart_operator(operator.get_full_name())

    """ Attach to the deployed pipeline, which blocks the execution until the
        pipeline is finished i.e., all operators are finished in the pipeline. """
    deployer.attach(pipeline.get_full_name(), on_operator_state_change=state_monitor)

    """ Destroy all pipeline related resources on Kubernetes """
    deployer.destroy(pipeline.get_full_name())
