import re

from release_history import VERSION_PATTERN


def release_heading(history, last_tag):
    heading = re.search(rf"^(#{{1,2}}) ({VERSION_PATTERN})[ \t]*$", history, re.M)
    if not heading or f"v{heading[2]}" != last_tag:
        raise SystemExit(f"The latest changelog heading must match {last_tag}.")
    return heading


def prepend_release(history, heading, version, notes):
    bullets = [f"- {note}" for note in notes]
    entry = "\n".join([f"{heading[1]} {version}", "", *bullets, "", ""])
    offset = heading.start()
    return history[:offset] + entry + history[offset:]
