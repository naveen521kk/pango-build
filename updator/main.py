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

from __future__ import annotations

import json
import logging
import os
import re
from packaging.version import Version
from pathlib import Path

import requests
import yaml
import version_filters

logging.basicConfig(level=logging.DEBUG)
DEPS_FILE = Path(__file__).parent / "dependency.yml"
FINAL_FILE = Path(__file__).resolve().parent.parent / "versions.json"
with open(DEPS_FILE) as f:
    logging.debug("Opening File at %s", DEPS_FILE.absolute())
    deps_info = yaml.load(f, Loader=yaml.FullLoader)
version_info = {}
github_headers = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"token {os.getenv('GITHUB_TOKEN')}",
}


class GithubHandler:
    def __init__(
        self,
        api_url: str,
        replace_in_files: dict,
        version_filters: version_filters.VersionFilter,
    ) -> None:
        self.api_url = api_url
        self.replace_in_files = replace_in_files
        self.version_filters = version_filters
        self.get_version()
        self.update_file()

    def get_version(self) -> None:
        version_re = re.compile(self.replace_in_files["tag_filter"]["matching"])
        logging.debug("Getting %s", self.api_url)
        content = requests.get(self.api_url, headers=github_headers).json()
        print(content)
        if content[0]["name"].startswith("v"):
            for i in range(len(content)):
                content[i]["name"] = content[i]["name"][1:]
        versions = [Version(i["name"]) for i in content if version_re.match(i["name"])]
        versions.sort()
        if self.version_filters.odd_minor_development:
            versions = [
                i for i in versions if version_filters.is_odd_minor_development(i)
            ]
        version = versions[-1]
        logging.info("Got Latest Version as %s", version)
        self.version = str(version)

    def update_file(self):
        logging.info(
            "Setting %s version  to %s", self.replace_in_files["name"], self.version
        )
        version_info[self.replace_in_files["name"]] = self.version


class GitlabHandler:
    def __init__(
        self,
        api_url: str,
        replace_in_files: dict,
        version_filters: version_filters.VersionFilter,
    ) -> None:
        self.api_url = api_url
        self.replace_in_files = replace_in_files
        self.version_filters = version_filters
        self.get_version()
        self.update_file()

    def get_version(self) -> None:
        version_re = re.compile(self.replace_in_files["tag_filter"]["matching"])
        logging.debug("Getting %s", self.api_url)
        content = requests.get(self.api_url).json()
        if content[0]["name"].startswith("v"):
            for i in range(len(content)):
                content[i]["name"] = content[i]["name"][1:]
        versions = [Version(i["name"]) for i in content if version_re.match(i["name"])]
        versions.sort()
        if self.version_filters.odd_minor_development:
            versions = [
                i for i in versions if not version_filters.is_odd_minor_development(i)
            ]
        version = versions[-1]
        logging.info("Got Latest Version as %s", version)
        self.version = str(version)

    def update_file(self):
        logging.info(
            "Setting %s version  to %s", self.replace_in_files["name"], self.version
        )
        version_info[self.replace_in_files["name"]] = self.version


for name in deps_info:
    lib = deps_info[name]
    if lib["type"] == "gitlab":
        GitlabHandler(
            lib["api_url"],
            replace_in_files=lib["replace_in_files"],
            version_filters=version_filters.VersionFilter(
                **{i: True for i in (lib["version_filters"] or [])}
            ),
        )
    else:
        GithubHandler(
            lib["api_url"],
            replace_in_files=lib["replace_in_files"],
            version_filters=version_filters.VersionFilter(
                **{i: True for i in (lib["version_filters"] or [])}
            ),
        )

with open(FINAL_FILE, "w") as f:
    data = json.dump(version_info, f, indent=4)
