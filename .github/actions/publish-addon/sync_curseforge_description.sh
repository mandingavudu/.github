#!/usr/bin/env bash

set -eo pipefail

metadata=$(jq -cn --rawfile description README.md \
  '{description: $description, descriptionType: "markdown"}')
status=$(curl --silent --show-error --max-time 30 --retry 2 \
  --output /dev/null --write-out '%{http_code}' \
  --header "X-Api-Token: $CF_API_TOKEN" \
  --form-string "metadata=$metadata" \
  "https://www.curseforge.com/api/projects/$PROJECT_ID/update-project")
if [[ "$status" != 2[0-9][0-9] ]]; then
  echo "::error::CurseForge description update returned HTTP $status."
  exit 1
fi
