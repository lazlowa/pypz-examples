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
from typing import Optional

from pypz.core.commons.parameters import OptionalParameter
from pypz.core.specs.operator import Operator
from pypz.plugins.kafka_io.ports import KafkaChannelInputPort
from pypz.plugins.loggers.default import DefaultLoggerPlugin


class DemoReaderOperator(Operator):
    """
    This operator reads avro records sent through Kafka by the writer
    operator and logs it to the stdout.
    """

    AvroSchemaString = """
    {
        "type": "record",
        "name": "DemoRecord",
        "fields": [
            {
                "name": "text",
                "type": "string"
            }
        ]
    }
    """

    raise_error_after_record_count = OptionalParameter(int,
                                                       alt_name="raiseErrorAfterRecordCount",
                                                       description="If set to a non-negative value, the operator will"
                                                                   "raise an error after it received the specified"
                                                                   "number of records")

    def __init__(self, name: str = None, *args, **kwargs):
        super().__init__(name, *args, **kwargs)

        self.input_port = KafkaChannelInputPort(schema=DemoReaderOperator.AvroSchemaString)
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
        By default the log level is INFO. One can change it via plugin parameter.
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

    def _on_error(self) -> None:
        """
        This method can be implemented to react to error events during
        execution. The error itself may come from arbitrary sources.
        """
        pass
