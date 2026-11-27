import re
import subprocess


VERSION_PATTERN = r"[0-9]+\.[0-9]+\.[0-9]+"
COMMIT_SUBJECT = re.compile(r"([a-z]+)(?:\([^)]*\))?(!)?: (.+)")
BREAKING_CHANGE = re.compile(r"^BREAKING[ -]CHANGE:", re.M)
PATCH, MINOR, MAJOR = 1, 2, 3
BUMP_BY_TYPE = {"feat": MINOR, "fix": PATCH, "perf": PATCH}


def _git(*args):
    return subprocess.check_output(["git", *args], text=True)


def latest_release_tag():
    stable_tags = [
        tag for tag in _git("tag", "--list", "v*").splitlines()
        if re.fullmatch(f"v{VERSION_PATTERN}", tag)
    ]
    if not stable_tags:
        raise SystemExit("Create an initial stable vX.Y.Z tag before enabling release preparation.")

    return _git(
        "describe", "--first-parent", "--tags", "--abbrev=0",
        *(f"--match={tag}" for tag in stable_tags),
    ).strip()


def release_changes(last_tag):
    level = 0
    notes = []
    commits = _git("log", "--first-parent", "--reverse", "-z", "--format=%B", f"{last_tag}..HEAD")
    for commit in commits.split("\0"):
        subject, _, body = commit.partition("\n")
        conventional = COMMIT_SUBJECT.fullmatch(subject)
        if not conventional:
            continue

        kind, breaking, title = conventional.groups()
        bump = MAJOR if breaking or BREAKING_CHANGE.search(body) else BUMP_BY_TYPE.get(kind, 0)
        if bump:
            level = max(level, bump)
            notes.append(title)

    return level, notes


def next_version(last_tag, bump):
    major, minor, patch = map(int, last_tag[1:].split("."))
    return {
        MAJOR: f"{major + 1}.0.0",
        MINOR: f"{major}.{minor + 1}.0",
        PATCH: f"{major}.{minor}.{patch + 1}",
    }[bump]
