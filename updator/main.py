import json
import logging
import re
from pathlib import Path

import requests
import yaml

logging.basicConfig(level=logging.DEBUG)
DEPS_FILE = Path(__file__).parent / "dependency.yml"
FINAL_FILE = Path(__file__).parent.parent / "versions.json"
with open(DEPS_FILE) as f:
    logging.debug("Opening File at %s", DEPS_FILE.absolute())
    deps_info = yaml.load(f, Loader=yaml.FullLoader)
version_info = {}


class GithubHandler:
    def __init__(self, api_url: str = None, replace_in_files: dict = None) -> None:
        self.api_url = api_url
        self.replace_in_files = replace_in_files
        self.get_version()
        self.update_file()

    def get_version(self) -> None:
        version_re = re.compile(self.replace_in_files["tag_filter"]["matching"])
        logging.debug("Getting %s", self.api_url)
        content = requests.get(self.api_url).json()
        for version in content:
            matching = version_re.match(version["name"])
            if matching:
                logging.info("Got Latest Version as %s", version["name"])
                self.version = version["name"]
                break

    def update_file(self):
        logging.info(
            "Setting %s version  to %s", self.replace_in_files["name"], self.version
        ) 
        version_info[self.replace_in_files["name"]] = self.version[1:] if self.version.startswith('v') else self.version


class GitlabHandler:
    def __init__(self, api_url: str = None, replace_in_files: dict = None) -> None:
        self.api_url = api_url
        self.replace_in_files = replace_in_files
        self.get_version()
        self.update_file()

    def get_version(self) -> None:
        version_re = re.compile(self.replace_in_files["tag_filter"]["matching"])
        logging.debug("Getting %s", self.api_url)
        content = requests.get(self.api_url).json()
        for version in content:
            matching = version_re.match(version["name"])
            if matching:
                logging.info("Got Latest Version as %s", version["name"])
                self.version = version["name"]
                break

    def update_file(self):
        logging.info(
            "Setting %s version  to %s", self.replace_in_files["name"], self.version
        )
        version_info[self.replace_in_files["name"]] = self.version[1:] if self.version.startswith('v') else self.version


for name in deps_info:
    lib = deps_info[name]
    if lib["type"] == "gitlab":
        GitlabHandler(lib["api_url"], replace_in_files=lib["replace_in_files"])
    else:
        GithubHandler(lib["api_url"], replace_in_files=lib["replace_in_files"])

with open(FINAL_FILE, "w") as f:

    data = json.dump(version_info, f, indent=4)
