"""Part of step 4: wait until the latest workflow run in Galaxy has finished, including its subworkflows.

Prints progress once a minute. At the end it lists any failed tools with the last line of their error,
and saves the run's id in galaxy_invocation.txt for the download.

Run from the final/ folder (called by scripts/04_run_workflow.sh):  python scripts/wait_for_run.py
"""
import collections
import sys
import time

import requests

URL = "http://localhost:8080/api"
KEY = {"key": open("galaxy_api_key.txt").read().strip()}
STILL_WORKING = {"new", "queued", "running", "waiting", "upload"}


def get(path, **params):
    response = requests.get(f"{URL}/{path}", params={**KEY, **params}, timeout=60)
    response.raise_for_status()
    return response.json()


def all_invocations(invocation_id):
    """The run itself and every subworkflow run inside it."""
    found = [invocation_id]
    for step in get(f"invocations/{invocation_id}")["steps"]:
        if step.get("subworkflow_invocation_id"):
            found += all_invocations(step["subworkflow_invocation_id"])
    return found


# the latest top-level run
latest = get("invocations", limit=1, sort_by="create_time", sort_desc="true", include_nested_invocations="false")[0]
run_id = latest["id"]
open("galaxy_invocation.txt", "w").write(run_id + "\n")
print("Waiting for Galaxy run", run_id)

while True:
    invocations = all_invocations(run_id)
    states = collections.Counter()
    for invocation_id in invocations:
        states.update(get(f"invocations/{invocation_id}/jobs_summary")["states"])
    scheduling = any(get(f"invocations/{i}")["state"] in ("new", "ready") for i in invocations)
    print(time.strftime("%H:%M"), "jobs:", dict(states), "(still scheduling)" if scheduling else "")
    if not scheduling and not STILL_WORKING & set(states):
        break
    time.sleep(60)

failed = [job for i in invocations for job in get("jobs", invocation_id=i, state="error")]
if failed or states.get("paused"):
    print()
    print("The run did not finish cleanly.")
    for job in failed:
        details = get(f"jobs/{job['id']}", full="true")
        last_line = (details.get("stderr") or "").strip().split("\n")[-1]
        print("  failed:", job["tool_id"].split("/")[-2], "-", last_line[:200])
    if states.get("paused"):
        print("  paused (waiting on a failed step):", states["paused"], "jobs")
    sys.exit(1)
print("The run finished: all jobs ok.")
