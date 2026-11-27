import os
from pathlib import Path

from changelog import prepend_release, release_heading
from release_history import latest_release_tag, next_version, release_changes


def main():
    last_tag = latest_release_tag()
    changelog = Path("CHANGELOG.md")
    history = changelog.read_text(encoding="utf-8")
    heading = release_heading(history, last_tag)

    bump, notes = release_changes(last_tag)
    if not bump:
        print(f"No release needed since {last_tag}.")
        return

    version = next_version(last_tag, bump)
    changelog.write_text(prepend_release(history, heading, version, notes), encoding="utf-8")
    with Path(os.environ["GITHUB_OUTPUT"]).open("a", encoding="utf-8") as output:
        print(f"version=v{version}", file=output)


if __name__ == "__main__":
    main()
