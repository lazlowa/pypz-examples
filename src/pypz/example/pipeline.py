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

from pypz.example.reader import DemoReaderOperator
from pypz.example.writer import DemoWriterOperator


class DemoPipeline(Pipeline):
    """
    A pipeline includes a set of operators that are (usually) connected to each other.
    """

    def __init__(self, name: str, *args, **kwargs):
        super().__init__(name, *args, **kwargs)

        # Notice that the "name" ctor argument is omitted, hence the framework
        # will use the variable's name as operator instance name
        self.reader = DemoReaderOperator()
        self.writer = DemoWriterOperator()

        """ Operator connections are defined on pipeline level. However one can
            dynamically define as well outside of the pipeline before execution or
            deployment."""
        self.reader.input_port.connect(self.writer.output_port)

        """ The parameter "operatorImageName" is required, if the operators are built
            into Docker images and deployed through container orchestration like Kubernetes"""
        self.reader.set_parameter("operatorImageName", "accessible-repository/pypz-example")
        self.writer.set_parameter("operatorImageName", "accessible-repository/pypz-example")

        """ The parameter "replicationFactor" can be used to create replicas of the operator.
            Note that a replicationFactor=3 means that along with the original 3 additional
            replicas will be created i.e., 4 operator instances will be created."""
        self.writer.set_parameter("replicationFactor", 3)
        self.reader.set_parameter("replicationFactor", 3)
