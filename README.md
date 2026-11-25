# ML Papers Archive

A curated personal archive of Machine Learning papers I have read, with notes, takeaways, and BibTeX references.

### Papers

Full list in **[PAPERS.md](PAPERS.md)**.

---

### Scripts

###### Add a new paper
```bash
# Interactive mode
python3 scripts/new_paper.py

# Or auto-fill metadata directly
python3 scripts/new_paper.py --arxiv 1706.03762
```

###### Rebuild the index after editing notes
```bash
python3 scripts/build_index.py
```

### Structure
```text
ml-papers/
├── README.md
├── PAPERS.md          # Auto-generated paper index
├── references.bib     # Consolidated BibTeX citations
├── notes/             # One Markdown note per paper
├── pdfs/              # Local PDFs (gitignored)
└── scripts/
    ├── new_paper.py   
    └── build_index.py
```
