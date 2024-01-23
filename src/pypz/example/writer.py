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
import time
from typing import Optional

from pypz.core.specs.operator import Operator
from pypz.plugins.kafka_io.ports import KafkaChannelOutputPort
from pypz.plugins.loggers.default import DefaultLoggerPlugin


class DemoWriterOperator(Operator):
    """
    This operator sends avro records to the receiving operators.
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

    def __init__(self, name: str = None, *args, **kwargs):
        super().__init__(name, *args, **kwargs)

        self.output_port = KafkaChannelOutputPort(schema=DemoWriterOperator.AvroSchemaString)
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
        record_to_send = {
            "text": "HelloWorld_" + str(self.output_record_count)
        }

        self.get_logger().info(f"Generated record: {record_to_send}")

        self.output_port.send([record_to_send])

        self.output_record_count += 1

        if 30 == self.output_record_count:
            return True

        time.sleep(1)

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

    def _on_error(self) -> None:
        """
        This method can be implemented to react to error events during
        execution. The error itself may come from arbitrary sources.
        """
        pass
