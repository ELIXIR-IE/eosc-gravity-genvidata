#!/usr/bin/env bash
# Step 4: run the workflow on the local Galaxy and download the outputs.
# Galaxy fetches the reads and sequences from ENA itself, using the addresses in inputs/job.yml.
# Run from the final/ folder:  bash scripts/04_run_workflow.sh
set -euo pipefail

URL="http://localhost:8080"
bash scripts/get_api_key.sh
API_KEY=$(cat galaxy_api_key.txt)
OUT="results/$(date +%Y-%m-%d_%H%M)"   # one folder per run
mkdir -p "$OUT"

# 1. copy the two IWC subworkflows into one native Galaxy file: workflow/genvidata.ga
python scripts/make_native_workflow.py

# 2. upload the inputs and start the workflow
#    ENA's servers sometimes refuse or drop a download, so try up to three times
for attempt in 1 2 3; do
    if planemo run workflow/genvidata.ga inputs/job.yml \
        --engine external_galaxy \
        --galaxy_url "$URL" \
        --galaxy_user_key "$API_KEY" \
        --history_name "GenViData $(date +%Y-%m-%d)" \
        --no_wait; then
        break
    fi
    if [ "$attempt" = 3 ]; then
        echo "Starting the run failed three times. See the messages above."
        exit 1
    fi
    echo "Attempt $attempt failed. Trying again in one minute ..."
    sleep 60
done

# 3. wait until every step has finished, including the steps inside the subworkflows
python scripts/wait_for_run.py

# 4. download the outputs
planemo invocation_download "$(cat galaxy_invocation.txt)" \
    --galaxy_url "$URL" \
    --galaxy_user_key "$API_KEY" \
    --output_directory "$OUT" \
    --output_json "$OUT/outputs.json"

echo "Outputs saved in $OUT. Next: python scripts/05_summarise.py"
