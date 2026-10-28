"""Part of step 4: turn the readable workflow (workflow/genvidata.gxwf.yml) into Galaxy's native format.

The readable file points to the two IWC workflows with "@import". This script copies them in,
so workflow/genvidata.ga is one self-contained file. It can also be uploaded into any Galaxy server
by hand (Workflows > Import).

Run from the final/ folder (called by scripts/04_run_workflow.sh):  python scripts/make_native_workflow.py
"""
import json
import os

from gxformat2.normalized._conversion import expanded_format2, to_native
from gxformat2.options import ConversionOptions

options = ConversionOptions(workflow_directory=os.path.abspath("workflow"))
expanded = expanded_format2("workflow/genvidata.gxwf.yml", options)   # copies in the @import files
native = to_native(expanded, options)
workflow = native.model_dump(by_alias=True, exclude_none=True, mode="json")


# One fix for newer Galaxy versions: the IWC ONT workflow's "Filter failed" step has no value for its
# optional "replacement" setting, and Galaxy 25 refuses to start a workflow with a missing setting.
# Here it is set to empty (no replacement), which is what the IWC workflow means.
def fill_filter_failed(steps):
    for step in steps.values():
        if step.get("subworkflow"):
            fill_filter_failed(step["subworkflow"]["steps"])
        if step.get("tool_id") == "__FILTER_FAILED_DATASETS__":
            state = step["tool_state"]
            state = json.loads(state) if isinstance(state, str) else state
            state.setdefault("replacement", None)
            step["tool_state"] = json.dumps(state)


fill_filter_failed(workflow["steps"])

with open("workflow/genvidata.ga", "w") as output_file:
    json.dump(workflow, output_file, indent=2)
print("Saved workflow/genvidata.ga")
