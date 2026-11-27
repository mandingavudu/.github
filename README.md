# Shared GitHub configuration

Shared repository settings and addon release automation for `mandingavudu`.

## Workflows

### addon-release

Prepares changelog pull requests, signs release tags after merge, and publishes tagged addons to CurseForge. [Workflow file](.github/workflows/addon-release.yml) · [Setup and release guide](docs/addon-release.md)

## Actions

### prepare-release

Calculates the next version from Conventional Commits and adds a changelog entry when a release is due. [Action file](.github/actions/prepare-release/action.yml)

### sign-release-tag

Validates the merged changelog commit, then signs and pushes its release tag. [Action file](.github/actions/sign-release-tag/action.yml)

### publish-addon

Packages and uploads tagged addons and syncs the CurseForge project description from the addon's README. [Action file](.github/actions/publish-addon/action.yml)
