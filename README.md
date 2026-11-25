# ML Papers Archive

A curated personal archive of Machine Learning papers I have read, with notes, takeaways, and BibTeX references.

### Papers

<!-- PAPERS:START -->
| Paper | Authors | Venue | Read |
| :--- | :--- | :--- | :---: |
| [**ImageNet Classification with Deep Convolutional Neural Networks**](notes/2012_krizhevsky_imagenet_classification_deep_convolutional.md) · [paper](https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf) | Krizhevsky, Sutskever, Hinton | NeurIPS 2012 | 2026-11-25 |
<!-- PAPERS:END -->

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
├── README.md          # Auto-generated paper index
├── references.bib     # Consolidated BibTeX citations
├── notes/             # One Markdown note per paper
├── pdfs/              # Local PDFs (gitignored)
└── scripts/
    ├── new_paper.py   
    └── build_index.py
```
