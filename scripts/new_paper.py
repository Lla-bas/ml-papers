#!/usr/bin/env python3
"""Create a new paper note from interactive prompts or an arXiv ID/URL."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

from build_index import update_index

ROOT = Path(__file__).resolve().parent.parent
NOTES_DIR = ROOT / "notes"
BIB_PATH = ROOT / "references.bib"


def slugify(text: str, max_words: int = 4) -> str:
    words = re.findall(r"[a-z0-9]+", text.lower())
    stop = {"a", "an", "the", "of", "for", "in", "on", "to", "with", "and", "is", "are"}
    filtered = [w for w in words if w not in stop] or words
    return "_".join(filtered[:max_words]) or "paper"


def extract_arxiv_id(raw: str) -> str | None:
    match = re.search(r"(\d{4}\.\d{4,5}(?:v\d+)?)", raw.strip())
    return match.group(1) if match else None


def fetch_arxiv_metadata(arxiv_id: str) -> dict[str, str]:
    url = f"https://export.arxiv.org/api/query?id_list={arxiv_id}"
    req = urllib.request.Request(url, headers={"User-Agent": "ml-papers-archive/1.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        xml_data = resp.read()

    ns = {"atom": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(xml_data)
    entry = root.find("atom:entry", ns)
    if entry is None:
        raise ValueError(f"No arXiv entry found for {arxiv_id}")

    title = re.sub(r"\s+", " ", (entry.findtext("atom:title", "", ns) or "").strip())
    published = (entry.findtext("atom:published", "", ns) or "").strip()
    year = published[:4] if len(published) >= 4 else str(dt.date.today().year)
    authors_list = [
        (a.findtext("atom:name", "", ns) or "").strip()
        for a in entry.findall("atom:author", ns)
    ]
    authors_list = [a for a in authors_list if a]

    if len(authors_list) == 0:
        short_authors = "Unknown"
    elif len(authors_list) == 1:
        short_authors = authors_list[0]
    elif len(authors_list) == 2:
        short_authors = f"{authors_list[0]} & {authors_list[1]}"
    else:
        last_name = authors_list[0].split()[-1]
        short_authors = f"{last_name} et al."

    return {
        "title": title,
        "authors": short_authors,
        "bib_authors": " and ".join(authors_list) or short_authors,
        "year": year,
        "venue": "arXiv",
        "url": f"https://arxiv.org/pdf/{arxiv_id}.pdf",
    }


def prompt(label: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{label}{suffix}: ").strip()
    return value or default


def make_cite_key(authors: str, year: str, title: str) -> str:
    first_token = re.sub(r"[^a-z0-9]", "", authors.split()[0].lower()) if authors else "paper"
    first_word = slugify(title, max_words=1)
    return f"{first_token}{year}{first_word}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Add a new paper note to ml-papers.")
    parser.add_argument("--arxiv", help="arXiv ID or URL (e.g. 1706.03762)")
    args = parser.parse_args()

    defaults: dict[str, str] = {
        "title": "",
        "authors": "",
        "bib_authors": "",
        "year": str(dt.date.today().year),
        "venue": "arXiv",
        "url": "",
    }

    if args.arxiv:
        arxiv_id = extract_arxiv_id(args.arxiv)
        if not arxiv_id:
            print(f"Could not parse arXiv ID from: {args.arxiv}", file=sys.stderr)
            return 1
        try:
            print(f"Fetching metadata for arXiv:{arxiv_id}...")
            defaults.update(fetch_arxiv_metadata(arxiv_id))
        except (urllib.error.URLError, ValueError, TimeoutError) as exc:
            print(f"Could not fetch from arXiv ({exc}); falling back to manual entry.")
            defaults["url"] = f"https://arxiv.org/pdf/{arxiv_id}.pdf"

    title = prompt("Title", defaults["title"])
    if not title:
        print("Title is required.", file=sys.stderr)
        return 1

    authors = prompt("Authors (e.g. Vaswani et al.)", defaults["authors"])
    year = prompt("Year", defaults["year"])
    venue = prompt("Venue (e.g. NeurIPS, ICML, arXiv)", defaults["venue"])
    url = prompt("Paper URL (arXiv / DOI)", defaults["url"])
    date_read = dt.date.today().isoformat()

    first_author = re.sub(r"[^a-z0-9]", "", authors.split()[0].lower()) if authors else "unknown"
    filename = f"{year}_{first_author}_{slugify(title)}.md"
    note_path = NOTES_DIR / filename

    if note_path.exists():
        print(f"Note already exists: {note_path}", file=sys.stderr)
        return 1

    cite_key = make_cite_key(authors, year, title)
    bib_authors = defaults["bib_authors"] or authors
    bib_entry = (
        f"@article{{{cite_key},\n"
        f"  title   = {{{title}}},\n"
        f"  author  = {{{bib_authors}}},\n"
        f"  year    = {{{year}}},\n"
        f"  journal = {{{venue}}},\n"
        f"  url     = {{{url}}}\n"
        f"}}"
    )

    note_content = (
        f"---\n"
        f'title: "{title}"\n'
        f'authors: "{authors}"\n'
        f"year: {year}\n"
        f'venue: "{venue}"\n'
        f'url: "{url}"\n'
        f"date_read: {date_read}\n"
        f"---\n\n"
        f"# {title}\n\n"
        f"\n\n"
        f"## Takeaways\n\n"
        f"\n\n"
        f"## Citation\n```bibtex\n{bib_entry}\n```\n"
    )

    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    note_path.write_text(note_content, encoding="utf-8")

    with BIB_PATH.open("a", encoding="utf-8") as bib_file:
        bib_file.write(f"\n{bib_entry}\n")

    count = update_index()
    print(f"\nCreated note: {note_path.relative_to(ROOT)}")
    print(f"Appended BibTeX entry '{cite_key}' to references.bib")
    print(f"Updated PAPERS.md ({count} paper(s) indexed).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
