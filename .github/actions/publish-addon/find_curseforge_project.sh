#!/usr/bin/env bash

set -eo pipefail

shopt -s nullglob
tocs=(./*.toc)
if (( ${#tocs[@]} == 0 )); then
  echo '::error::Expected an addon TOC in the repository root.'
  exit 1
fi
project_id=$(sed -nE 's/^## X-Curse-Project-ID:[[:space:]]*([0-9]+)[[:space:]]*$/\1/p' "${tocs[@]}" | sort -u)
if [[ ! "$project_id" =~ ^[0-9]+$ ]]; then
  echo '::error::Expected one numeric CurseForge project ID in the addon TOCs.'
  exit 1
fi
printf 'id=%s\n' "$project_id" >> "$GITHUB_OUTPUT"
