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

### Using the pypz python base image ###
FROM lazlowa/pypz-python-dev:latest

### Copying project context ###
COPY dist/* ./
RUN pip install ./*.whl

### Setting entry point and command ###
# You shall always set the entry point and command like below.
# The startup script comes from the base image and ensures the
# proper starting of the operator executor.
ENTRYPOINT ["/bin/bash"]
CMD ["pypz-startup.sh"]