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
from typing import Optional, Any

from pypz.core.commons.parameters import RequiredParameter, OptionalParameter
from pypz.core.specs.operator import Operator
from pypz.core.specs.pipeline import Pipeline
from pypz.plugins.loggers.default import DefaultLoggerPlugin
from pypz.plugins.rmq_io.ports import RMQChannelOutputPort, RMQChannelInputPort


class RMQDemoWriterOperator(Operator):
    """
    This operator sends avro records to the receiving operators.
    """

    record_count = RequiredParameter(int, alt_name="recordCount",
                                     description="Specifies number of records to send")
    message = OptionalParameter(str, description="Specifies the message prefix for the record")

    def __init__(self, name: str = None, *args, **kwargs):
        super().__init__(name, *args, **kwargs)

        self.output_port = RMQChannelOutputPort()
        """
        An output port enables the operator to send data to other operators. 
        The connection is usually established on the pipeline level.
        """

        self.output_record_count: int = 0

        self.logger = DefaultLoggerPlugin()
        """
        A logger plugin enables the framework to handle logs from the framework. The default
        logger puts the messages to stdout.
        """

        self.record_count = None
        """
        Since it is a required parameter, the initial value does not matter.
        """

        self.message = "HelloWorld"
        """
        This is an optional parameter, the default value is the initial value of the variable.
        """

    def _on_init(self) -> bool:
        """
        This method shall implement the logic to initialize the operation.

        :return: True succeeded, False if more iteration required (to not block the execution)
        """
        return True

    def _on_running(self) -> Optional[bool]:
        """
        This method shall implement the actual processing logic.

        :return: True succeeded, False if more iteration required (to not block the execution), None if
        framework shall decide
        """
        record_to_send = f"{self.message}_{self.output_record_count}"

        self.get_logger().info(f"Generated record: {record_to_send}")

        self.output_port.send([record_to_send])

        self.output_record_count += 1

        if self.record_count == self.output_record_count:
            return True

        return False

    def _on_shutdown(self) -> bool:
        """
        This method shall implement the logic to shut down the operation.

        :return: True succeeded, False if more iteration required (to not block the execution)
        """
        return True

    def _on_interrupt(self, system_signal: int = None) -> None:
        """
        This method can be implemented to react to interrupt signals like
        SIGINT, SIGTERM etc. The specs implementation can then execute interrupt
        logic e.g., early termination of loops.

        :param system_signal: id of the system signal that causes interrupt
        """
        pass

    def _on_error(self, source: Any, exception: Exception) -> None:
        """
        This method can be implemented to react to error events during
        execution. The error itself may come from arbitrary sources.
        """
        pass


class RMQDemoReaderOperator(Operator):
    """
    This operator reads avro records sent through Kafka by the writer
    operator and logs it to the stdout.
    """

    raise_error_after_record_count = OptionalParameter(int,
                                                       alt_name="raiseErrorAfterRecordCount",
                                                       description="If set to a non-negative value, the operator will"
                                                                   "raise an error after it received the specified"
                                                                   "number of records")

    def __init__(self, name: str = None, *args, **kwargs):
        super().__init__(name, *args, **kwargs)

        self.input_port = RMQChannelInputPort()
        """
        An input port enables the operator to receive data from other operators' output port.
        The connection is usually established on the pipeline level.
        Notice that the "name" ctor argument is omitted, hence the framework
        will use the variable's name as operator instance name.
        """

        self.logger = DefaultLoggerPlugin()
        """
        A logger plugin enables the framework to handle logs from the framework. The default
        logger puts the messages to stdout.
        """

        self.logger.set_parameter("logLevel", "DEBUG")
        """
        By default, the log level is INFO. One can change it via plugin parameter.
        """

        self.received_record_count = 0
        """
        Stores, how many records have been received
        """

        self.raise_error_after_record_count = None

    def _on_init(self) -> bool:
        """
        This method shall implement the logic to initialize the operation.
        :return: True succeeded, False if more iteration required (to not block the execution)
        """
        return True

    def _on_running(self) -> Optional[bool]:
        """
        This method shall implement the actual processing logic.
        :return: True succeeded, False if more iteration required (to not block the execution), None if
        framework shall decide
        """
        records = self.input_port.retrieve()

        self.received_record_count += len(records)

        if ((self.raise_error_after_record_count is not None) and
                (self.raise_error_after_record_count <= self.received_record_count)):
            raise BrokenPipeError(f"Test error after received the specified record count: "
                                  f"{self.raise_error_after_record_count} / {self.received_record_count}")

        for record in records:
            self.get_logger().debug(f"Received record: {record}")

        return None

        # Returning None is equivalent to the following:
        # return not self.input_port.can_retrieve()

    def _on_shutdown(self) -> bool:
        """
        This method shall implement the logic to shut down the operation.
        :return: True succeeded, False if more iteration required (to not block the execution)
        """
        return True

    def _on_interrupt(self, system_signal: int = None) -> None:
        """
        This method can be implemented to react to interrupt signals like
        SIGINT, SIGTERM etc. The specs implementation can then execute interrupt
        logic e.g., early termination of loops.
        :param system_signal: id of the system signal that causes interrupt
        """
        pass

    def _on_error(self, source: Any, exception: Exception) -> None:
        """
        This method can be implemented to react to error events during
        execution. The error itself may come from arbitrary sources.
        """
        pass


class RMQDemoPipeline(Pipeline):
    """
    A pipeline includes a set of operators that are (usually) connected to each other.
    """

    def __init__(self, name: str, *args, **kwargs):
        super().__init__(name, *args, **kwargs)

        """ Notice that the "name" ctor argument is omitted, hence the framework
            will use the variable's name as operator instance name """
        self.reader = RMQDemoReaderOperator()
        self.writer = RMQDemoWriterOperator()

        """ Operator connections are defined on pipeline level. However, one can
            dynamically define as well outside the pipeline before execution or
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
        self.reader.set_parameter("replicationFactor", 50)
