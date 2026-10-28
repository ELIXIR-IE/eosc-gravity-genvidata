#!/usr/bin/env bash
# Step 3: start a Galaxy server in Docker and install the tools the workflow needs.
# Galaxy's data and installed tools are kept in final/galaxy_storage, so a restart reuses them.
# Galaxy is only reachable from this computer (127.0.0.1), because it uses the image's default admin login.
# Run from the final/ folder:  bash scripts/03_start_galaxy.sh
set -euo pipefail

IMAGE="quay.io/bgruening/galaxy:25.1.1"
NAME="genvidata-galaxy"
URL="http://localhost:8080"
STORAGE="$(pwd)/galaxy_storage"

# 1. start the container, unless it is already running
mkdir -p "$STORAGE"
if [ -z "$(docker ps -q -f name=^${NAME}$)" ]; then
    if [ -n "$(docker ps -aq -f name=^${NAME}$)" ]; then
        docker start "$NAME"
    else
        docker run -d --name "$NAME" -p 127.0.0.1:8080:80 -v "$STORAGE":/export "$IMAGE"
    fi
fi

# 2. wait until Galaxy answers
echo "Waiting for Galaxy at $URL ..."
until curl -s -f "$URL/api/version" > /dev/null; do
    sleep 10
done
echo "Galaxy is up: $(curl -s "$URL/api/version")"

# 3. read the admin user's API key (the image resets it each time the container starts)
bash scripts/get_api_key.sh
API_KEY=$(cat galaxy_api_key.txt)

# 4. install the tools (first time: this can take an hour or more)
shed-tools install -g "$URL" -a "$API_KEY" -t workflow/tools.yml

# 5. install each tool's software (conda packages) and list any that fail
python scripts/install_tool_dependencies.py
bash scripts/fix_old_tool_envs.sh

# 6. restart Galaxy, so that every Galaxy process (including the one that runs workflows) sees the new tools
docker restart "$NAME"
until curl -s -f "$URL/api/version" > /dev/null; do
    sleep 10
done

echo "Done. Open $URL in a browser to watch runs (log in as admin@example.org / password)."
