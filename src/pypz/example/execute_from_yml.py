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
from pypz.core.specs.pipeline import Pipeline
from pypz.executors.pipeline.executor import PipelineExecutor

"""
This example shows, how to create a Pipeline instance object from a configuration
stored in a yaml file and, how to execute it locally with the PipelineExecutor.
Note that you should use PipelineExecutor for testing and not for productive workload.
"""

if __name__ == "__main__":
    with open('../../../pipeline.yml') as yml_file:
        pipeline = Pipeline.create_from_string(yml_file.read())

    """ Note that you will not be able to execute this pipeline until 
        you did not modify the parameters in the YAML file. You need 
        to set the 'channelLocation' parameter! """

    executor = PipelineExecutor(pipeline)
    executor.start()
    executor.shutdown()
