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

from pypz.core.specs.operator import Operator
from pypz.plugins.kafka_io.ports import KafkaChannelInputPort
from pypz.plugins.loggers.default import DefaultLoggerPlugin


class DemoReaderOperator(Operator):

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

        self.input_port = KafkaChannelInputPort(schema=DemoReaderOperator.AvroSchemaString)

        self.logger = DefaultLoggerPlugin()
        self.logger.set_parameter("logLevel", "DEBUG")

    def _on_init(self) -> bool:
        return True

    def _on_running(self) -> Optional[bool]:
        records = self.input_port.retrieve()
        for record in records:
            self.get_logger().debug(f"Received record: {record}")
            # return not self.input_port.can_retrieve()
        return None

    def _on_shutdown(self) -> bool:
        return True

    def _on_interrupt(self, system_signal: int = None) -> None:
        pass

    def _on_error(self) -> None:
        pass


