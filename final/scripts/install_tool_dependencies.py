"""Part of step 3: ask Galaxy to install the conda packages for every tool the workflow uses.

Installing a Tool Shed repository only registers the tool. Its software (for example medaka or minimap2)
is installed separately, here, one tool at a time, so any tool that fails is listed at the end.

Run from the final/ folder (called by scripts/03_start_galaxy.sh):  python scripts/install_tool_dependencies.py
"""
import json
import time

import requests
import yaml

URL = "http://localhost:8080"
API_KEY = open("galaxy_api_key.txt").read().strip()

# every tool id in the two IWC workflows and in our own workflow
tool_ids = set()
for path in ["workflow/iwc/ont-artic-variation.ga", "workflow/iwc/consensus-from-variation.ga"]:
    for step in json.load(open(path))["steps"].values():
        if step.get("tool_shed_repository"):
            tool_ids.add(step["tool_id"])
for step in yaml.safe_load(open("workflow/genvidata.gxwf.yml"))["steps"].values():
    if "tool_id" in step:
        tool_ids.add(step["tool_id"])

failed = []
for number, tool_id in enumerate(sorted(tool_ids), start=1):
    short_name = "/".join(tool_id.split("/")[-2:])
    start = time.time()
    response = requests.post(f"{URL}/api/tools/{requests.utils.quote(tool_id, safe='')}/dependencies",
                             params={"key": API_KEY}, timeout=3600)
    if response.ok:
        states = [d.get("dependency_type") or "missing" for d in response.json()]
        print(f"({number}/{len(tool_ids)}) {short_name}: {', '.join(states)} ({time.time() - start:.0f} s)")
        if "missing" in states or "null" in states:
            failed.append(short_name)
    else:
        print(f"({number}/{len(tool_ids)}) {short_name}: FAILED {response.status_code} {response.text[:200]}")
        failed.append(short_name)

print()
print("Tools with missing software:", ", ".join(failed) if failed else "none")
