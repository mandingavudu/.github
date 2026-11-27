#!/usr/bin/env bash

set -eo pipefail

if [[ $(git diff --name-only HEAD^ HEAD) != CHANGELOG.md ]]; then
  echo '::error::The release commit must change only CHANGELOG.md.'
  exit 1
fi

version=$(awk '/^#{1,2} [0-9]+\.[0-9]+\.[0-9]+[[:space:]]*$/ {print "v" $2; exit}' CHANGELOG.md)
if [[ -z "$version" || "$PR_TITLE" != "chore(release): add $version changelog" ]]; then
  echo '::error::The release PR title must match the latest changelog version.'
  exit 1
fi

if git show-ref --verify --quiet "refs/tags/$version"; then
  if [[ $(git rev-parse "refs/tags/${version}^{commit}") != "$(git rev-parse HEAD)" ]]; then
    echo "::error::$version already points to a different commit."
    exit 1
  fi
  exit 0
fi

key_file=$(mktemp)
trap 'rm -f "$key_file"' EXIT
printf '%s\n' "$SIGNING_KEY" > "$key_file"
git -c "user.name=$GITHUB_REPOSITORY_OWNER" \
    -c "user.email=$SIGNING_EMAIL" \
    -c gpg.format=ssh \
    -c "user.signingkey=$key_file" \
    tag -s -m '' "$version" HEAD
git push --no-follow-tags origin "refs/tags/$version:refs/tags/$version"
