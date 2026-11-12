"""Save a Jira report locally without replacing an earlier report.

The caller supplies complete Markdown in a private local file. This helper never
reads Jira or publishes the report; it prints only the created artifact path.
"""

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


FORMATS = {"summary", "by-contributor", "brief"}


def save_report(source, destination, root, start, end, format_name, generated_at=None, project_label=False):
    """Exclusively create a timestamped Markdown report, retrying name collisions."""
    if project_label:
        slug = re.sub(r"[^a-z0-9]+", "-", root.casefold()).strip("-")
        if not slug:
            raise ValueError("Project label needs a filesystem-safe name")
        selector = f"label-{slug}"
    else:
        if not re.fullmatch(r"[A-Z][A-Z0-9]+-\d+", root):
            raise ValueError("Root must be a Jira key")
        selector = root
    for value in (start, end):
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value) or datetime.strptime(value, "%Y-%m-%d").strftime("%Y-%m-%d") != value:
            raise ValueError("Dates must be ISO calendar dates (YYYY-MM-DD)")
    if format_name not in FORMATS:
        raise ValueError("Unsupported report format")

    content = Path(source).read_text(encoding="utf-8")
    directory = Path(destination)
    directory.mkdir(parents=True, exist_ok=True)
    instant = generated_at or datetime.now(timezone.utc)
    stamp = instant.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    stem = f"{selector}_{start}_{end}_{format_name}_{stamp}"
    for suffix in range(10000):
        name = f"{stem}{'_' + str(suffix) if suffix else ''}.md"
        path = directory / name
        created = False
        try:
            with path.open("x", encoding="utf-8") as report:
                created = True
                report.write(content)
            return path
        except FileExistsError:
            continue
        except OSError:
            if created:
                path.unlink()
            raise
    raise RuntimeError("Too many report filename collisions")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", help="Jira root key (or project label with --project-label)")
    parser.add_argument("--project-label", action="store_true", help="interpret root argument as a project label")
    parser.add_argument("start")
    parser.add_argument("end")
    parser.add_argument("format", choices=sorted(FORMATS))
    parser.add_argument("--source", type=Path, required=True, help="private local file containing the complete report text")
    parser.add_argument("--destination", type=Path, default=Path("reports"))
    args = parser.parse_args()
    try:
        path = save_report(args.source, args.destination, args.root, args.start, args.end, args.format,
                           project_label=args.project_label)
    except (OSError, ValueError, RuntimeError) as error:
        print(f"Report not saved: {error}", file=sys.stderr)
        return 1
    print(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
