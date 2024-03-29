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
from pypz.sniffer.viewer import PipelineSnifferViewer

from pypz.deployers.k8s import KubernetesDeployer

"""
This example shows, how to use the IO Sniffer to visualize the states of the
operators' IO ports. In addition, it retrieves a pipeline instance deployed
on Kubernetes instead of creating an object in the code. This ensures
consistency, since it you would have a pipeline instance, which you deploy
and an other instance from the same spec, which you sniff, the you always
need to make sure that the same parameters are set for both, which is
error prone.
"""

if __name__ == "__main__":
    deployer = KubernetesDeployer(namespace="NAMESPACE")

    """ The deployed pipeline will be retrieved by name and a Pipeline object will be created """
    pipeline = deployer.retrieve_deployed_pipeline("pipeline")

    """ The IO sniffer is used to monitor the ports' activities like in what states
        are the ports in, how many records have been sent/received etc. This tool
        is useful to understand the behaviour of the pipeline. """
    sniffer = PipelineSnifferViewer(pipeline)

    sniffer.mainloop()
