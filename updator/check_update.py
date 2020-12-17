import requests
import json
import os
from pathlib import Path

access_token = os.getenv("GITHUB_TOKEN")
FINAL_FILE = Path(__file__).parent.parent / "versions.json"
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
