# Shared addon release workflow

## Caller workflow

Add the caller below as `.github/workflows/release.yml` in an addon repository. The example checks for releases on Mondays at 11:00 p.m. local time in Irvine, California, and on manual runs from `main`. Adjust `cron` and `timezone` to choose your schedule. After GitHub squash-merges the changelog PR, the workflow signs an empty-message tag on the merged commit. A `v*` tag push packages the addon, publishes it to CurseForge, and syncs its description from `README.md`. Select **Sync only the CurseForge description** for a description-only run.

```yaml
name: Release

on:
  schedule:
    - cron: '0 23 * * 1'
      timezone: America/Los_Angeles
  workflow_dispatch:
    inputs:
      description-only:
        description: Sync only the CurseForge description
        type: boolean
        default: false
  pull_request:
    branches: [main]
    types: [closed]
  push:
    tags: ['v*']

jobs:
  release:
    uses: mandingavudu/.github/.github/workflows/addon-release.yml@main
    permissions:
      contents: write
    with:
      app-client-id: ${{ vars.RELEASE_APP_CLIENT_ID }}
      signing-email: ${{ vars.RELEASE_SIGNING_EMAIL }}
      description-only: ${{ inputs.description-only == true }}
      install-libeqol: ${{ vars.RELEASE_INSTALL_LIBEQOL == 'true' }}
    secrets:
      app-private-key: ${{ secrets.RELEASE_APP_PRIVATE_KEY }}
      signing-key: ${{ secrets.RELEASE_SIGNING_KEY }}
      curseforge-token: ${{ secrets.CF_API_TOKEN }}
```

## Set up the release GitHub App

The GitHub App gives the workflow a bot identity for opening changelog PRs and pushing automated release tags. The workflow uses the app's credentials to request a short-lived installation token. A tag push made with that token can start the CurseForge publishing workflow. [GitHub's workflow trigger rules](https://docs.github.com/en/actions/concepts/security/github_token#when-github_token-triggers-workflow-runs)

1. Open **Settings → Developer settings → GitHub Apps → New GitHub App** for the GitHub account or organization that owns the addon repositories. Pick a name and use the owner's GitHub profile or organization URL as the homepage.
2. Turn off **Webhook → Active**. Under **Repository permissions**, set **Contents** and **Pull requests** to **Read and write**. Choose **Only on this account**, then create the app. [GitHub App registration](https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/registering-a-github-app)
3. On the app's **General** page, copy the **Client ID**. Under **Private keys**, select **Generate a private key** to download the `.pem` file. [GitHub App private keys](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/managing-private-keys-for-github-apps#generating-private-keys)
4. Open the app's **Install App** page, select the repository owner, then choose **Only select repositories** and select the addon repositories that will use this workflow. The same app can serve multiple addon repositories. [GitHub App installation](https://docs.github.com/en/apps/using-github-apps/installing-your-own-github-app)

## Configure each addon repository

Enable squash merging and auto-merge in the repository's **Settings → General**. Add the values below under **Settings → Secrets and variables → Actions**. The app's private key authenticates the bot to GitHub, and the separate SSH signing key signs the Git tag.

| Name | Type | Value |
| --- | --- | --- |
| `RELEASE_APP_CLIENT_ID` | Variable | Release GitHub App client ID |
| `RELEASE_SIGNING_EMAIL` | Variable | Email of the GitHub account that owns the SSH signing key |
| `RELEASE_INSTALL_LIBEQOL` | Variable | `true` for addons that install LibEQOL into `Libs` during packaging |
| `RELEASE_APP_PRIVATE_KEY` | Secret | Full contents of the GitHub App's downloaded `.pem` file |
| `RELEASE_SIGNING_KEY` | Secret | SSH private signing key with the public key registered on GitHub as a signing key |
| `CF_API_TOKEN` | Secret | CurseForge API token |

## Versioning and publishing

Release preparation starts from the latest stable `vX.Y.Z` tag on the first-parent history of `main`. The first release heading in `CHANGELOG.md` must match that tag and use `# X.Y.Z` or `## X.Y.Z`. A breaking Conventional Commit triggers a major bump, `feat` triggers a minor bump, and `fix` or `perf` triggers a patch bump. Weeks with only other changes leave the changelog alone. Publishing reads the CurseForge project ID from `X-Curse-Project-ID` in the root TOC files.

## Release from a manual tag

Merge the changelog-only release commit into `main`. Make sure the latest heading in `CHANGELOG.md` matches the version you plan to tag so the next automated release can calculate its version.

From the release commit, create and push a signed tag with an empty message. Replace `v1.4.1` with your release version.

```bash
git tag -s -m '' v1.4.1
git push origin refs/tags/v1.4.1
```

Pushing a manual `v*` tag packages and uploads the addon to CurseForge. After the upload succeeds, the workflow updates the CurseForge project description from `README.md` at the tagged commit.
