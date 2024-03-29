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
from pypz.executors.pipeline.executor import PipelineExecutor

from pypz.example.pipeline import DemoPipeline

"""
This example shows, how to get and display the parameter schema of an instance.
This might be useful, if you are uncertain, what parameters can/shall be
configured for the given instance.
"""

if __name__ == "__main__":
    """ Notice that unlike in the case of plugins and operators, the "name" ctor argument
        is defined here. The reason is that to use the variables' name as instance name,
        we need to control the context, where the variable is set. This is the case for
        plugins and operators, but not for pipelines, hence it is required to provide
        an instance name for pipelines."""
    pipeline = DemoPipeline("pipeline")

    """ You can check the parameter schema like this. It will print out all the expected parameters.
        Notice that the term expected parameter covers both the required and optional parameters. """
    print(pipeline.writer.get_expected_parameters())
    print(pipeline.reader.input_port.get_expected_parameters())
