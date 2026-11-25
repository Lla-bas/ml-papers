#!/usr/bin/env python3
"""Rebuild the paper index table in PAPERS.md from notes/*.md frontmatter."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTES_DIR = ROOT / "notes"
INDEX_PATH = ROOT / "PAPERS.md"

START_MARKER = "<!-- PAPERS:START -->"
END_MARKER = "<!-- PAPERS:END -->"


def parse_frontmatter(text: str) -> dict[str, object]:
    """Parse simple YAML frontmatter without external dependencies."""
    match = re.match(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", text, re.DOTALL)
    if not match:
        return {}

    data: dict[str, object] = {}
    for raw_line in match.group(1).splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, raw_val = line.split(":", 1)
        key = key.strip()
        val = raw_val.strip()

        if val.startswith("[") and val.endswith("]"):
            items = [
                item.strip().strip("\"'")
                for item in val[1:-1].split(",")
                if item.strip().strip("\"'")
            ]
            data[key] = items
        else:
            val = val.strip("\"'")
            if key == "year" and val.isdigit():
                data[key] = int(val)
            else:
                data[key] = val
    return data


def escape_md(value: str) -> str:
    return value.replace("|", "\\|").strip()


def collect_papers() -> list[dict[str, object]]:
    papers: list[dict[str, object]] = []
    if not NOTES_DIR.exists():
        return papers

    for path in sorted(NOTES_DIR.glob("*.md")):
        if path.name.startswith("_"):
            continue
        meta = parse_frontmatter(path.read_text(encoding="utf-8"))
        if not meta.get("title"):
            continue
        meta["_path"] = path.relative_to(ROOT).as_posix()
        papers.append(meta)

    papers.sort(
        key=lambda p: (
            str(p.get("date_read", "")),
            int(p.get("year", 0)) if isinstance(p.get("year"), int) else 0,
            str(p.get("title", "")).lower(),
        ),
        reverse=True,
    )
    return papers


def render_index(papers: list[dict[str, object]]) -> str:
    if not papers:
        return (
            "_No papers archived yet. Run `python3 scripts/new_paper.py` to add your first note!_"
        )

    lines: list[str] = [
        "| Paper | Authors | Venue | Read |",
        "| :--- | :--- | :--- | :---: |",
    ]

    for p in papers:
        title = escape_md(str(p.get("title", "Untitled")))
        note_path = str(p["_path"])
        url = str(p.get("url", "")).strip()
        title_cell = f"[**{title}**]({note_path})"
        if url:
            title_cell += f" · [download]({url})"

        authors = escape_md(str(p.get("authors", "—")))
        venue_parts = [str(p.get("venue", "")).strip(), str(p.get("year", "")).strip()]
        venue = escape_md(" ".join(part for part in venue_parts if part) or "—")
        date_read = escape_md(str(p.get("date_read", "—")))

        lines.append(f"| {title_cell} | {authors} | {venue} | {date_read} |")

    return "\n".join(lines)


def update_index() -> int:
    papers = collect_papers()
    rendered = render_index(papers)
    block = f"{START_MARKER}\n{rendered}\n{END_MARKER}"

    if not INDEX_PATH.exists():
        INDEX_PATH.write_text(f"# Papers\n\n{block}\n", encoding="utf-8")
        return len(papers)

    content = INDEX_PATH.read_text(encoding="utf-8")
    pattern = re.compile(
        rf"{re.escape(START_MARKER)}.*?{re.escape(END_MARKER)}", re.DOTALL
    )
    if pattern.search(content):
        new_content = pattern.sub(block, content, count=1)
    else:
        new_content = content.rstrip() + f"\n\n{block}\n"

    INDEX_PATH.write_text(new_content, encoding="utf-8")
    return len(papers)


if __name__ == "__main__":
    count = update_index()
    print(f"Updated PAPERS.md with {count} paper(s).")
