#!/usr/bin/env bash
# Reads the API key of Galaxy's admin user (admin@example.org) and saves it in galaxy_api_key.txt.
# The Galaxy Docker image resets this key every time the container starts, so steps 3 and 4 read it fresh.
# Run from the final/ folder (called by scripts/03_start_galaxy.sh and scripts/04_run_workflow.sh).
set -euo pipefail

URL="http://localhost:8080"
BOOTSTRAP_KEY="HSNiugRFvgT574F43jZ7N9F3"   # the image's built-in admin key, only usable from this computer

USER_ID=$(curl -s "$URL/api/users?key=$BOOTSTRAP_KEY" | python -c "import json,sys; print(json.load(sys.stdin)[0]['id'])")
curl -s "$URL/api/users/$USER_ID/api_key/detailed?key=$BOOTSTRAP_KEY" \
    | python -c "import json,sys; print(json.load(sys.stdin)['key'])" > galaxy_api_key.txt
echo "API key saved in galaxy_api_key.txt"
