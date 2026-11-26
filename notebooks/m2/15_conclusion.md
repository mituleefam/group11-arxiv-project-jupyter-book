---
title: "Chapter 15: Milestone 2 Conclusion"
short_title: "15. Conclusion"
---

## 1. Achievements

- **Hierarchical parsing runs on the group's whole corpus:** each version is read along LaTeX's actual compilation
  path (root file, `\input`/`\include`, subfiles) and built into a tree with clear levels, including appendices,
  abstracts and lists. Versions without TeX still get a root node instead of being dropped.
- **Standardization:** formatting commands are removed, formulas come in two uniform forms (`$...$` and
  `equation`), and sentences are split without cutting inside formulas, commands, abbreviations, URLs or decimal
  numbers.
- **References:** `\bibitem`, amsrefs, `.bib` and `.bbl` all end up in one BibTeX form; duplicate references across
  versions are merged with the union of their fields, and every `\cite` is renamed to the canonical key.
- **Content deduplication:** identical elements across versions share one `element_id`, while the `hierarchy` table
  stays a proper tree in each version.
- **Validation and measurement:** `validate_m2.py` checks the trees, the references and the Parquet schema;
  `benchmark_m2.py` measures wall time, RAM and output size on CPU-only Colab, with one code commit for all five
  ranges.

The numbers are in [Chapter 12](./12_results.ipynb) (parsing success rate, before and after deduplication) and
[Chapter 13](./13_performance.ipynb) (performance).

## 2. Remaining limitations

The full list is in [Chapter 14](./14_validation.ipynb). In summary:

- Missing source files (an included file, a `.bib` or a `.bbl` absent from the arXiv package) cannot be read.
- Fields of free-form `\bibitem` entries are extracted by rules and can be wrong for unusual formats.
- In at least 16 papers the reference list uses a form that the parser does not recognize and remains in the tree; 81
  papers type their references by hand and yield no BibTeX entry.
- Paper 2605.16616 reprints `.bbl` code in a figure and an appendix: the `bibliography_exclusion` check gives a false
  positive and the `bibtex` table has one extra entry, which Milestone 3 drops when loading the data.

## 3. Towards Milestone 3

- The **`bibtex`** table provides the entries cited by each paper, and `references.json` of Milestone 1 (Semantic
  Scholar, with arXiv IDs) provides the candidate references. Milestone 3 matches each BibTeX entry with the arXiv ID
  of the reference it denotes.
- The `title`, `authors` and `year` fields standardized in Milestone 2 are the basis of the matching features; DOIs
  and arXiv IDs, when present, allow automatic labelling.
- The three tables `elements`, `hierarchy` and `bibtex` are uploaded to Hugging Face with the other tables of the
  dataset.
