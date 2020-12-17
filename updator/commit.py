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
