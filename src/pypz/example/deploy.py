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

if __name__ == "__main__":
    pipeline = DemoPipeline("pipeline")
    pipeline.set_parameter(">>channelLocation", "KAFKA_BROKER_URL")

    deployer = KubernetesDeployer(namespace="NAMESPACE")

    if not deployer.is_deployed(pipeline.get_full_name()):
        deployer.deploy(pipeline)

    deployer.attach(pipeline.get_full_name())
    deployer.destroy(pipeline.get_full_name())
