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
import os
from pathlib import Path

access_token = os.getenv("GITHUB_TOKEN")
FINAL_FILE = Path(__file__).resolve().parent.parent / "versions.json"
API_URL = "https://api.github.com/repos/naveen521kk/pango-build/releases"
headers = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"token {access_token}",
}
with open(FINAL_FILE, "r") as f:
    data = json.load(f)
pango_version = data["pango"]

content = requests.get(API_URL, headers=headers).json()
tags = [i["tag_name"] for i in content]
if f"v{pango_version}" not in tags:
    print("true")
else:
    print("false")
