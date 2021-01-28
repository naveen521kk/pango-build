# Copyright 2021 Naveen M K

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requests
import json
from pathlib import Path

COMMIT_MESSAGE = ""

URL = "https://raw.githubusercontent.com/naveen521kk/pango-build/master/versions.json"
VERSION_FILE = Path(__file__).resolve().parent.parent / "versions.json"
pre_content = requests.get(URL).json()

with open(VERSION_FILE) as f:
    current_content = json.load(f)

for name in pre_content:
    if pre_content[name] != current_content[name]:
        COMMIT_MESSAGE += f"Update {name} to {current_content[name]}\n"
print(COMMIT_MESSAGE)
