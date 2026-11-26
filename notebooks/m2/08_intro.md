---
title: "Chapter 8: Introduction to Milestone 2"
short_title: "8. Introduction"
---

> **Phase:** Milestone 2 — Hierarchical Parsing and Standardization
> **Input:** the LaTeX corpus of Milestone 1 (5 ranges × 5,000 arXiv IDs)
> **Output:** three Parquet tables `elements`, `hierarchy`, `bibtex`

## 1. Members and responsibilities

As in Milestone 1, each member leads one group of modules. Every module follows a shared interface
(`src/m2_contract.py`), which allowed the modules to be developed in parallel and the pipeline to run before every
module was complete.

| No. | Full name | Main role | Modules | Chapter |
| :---: | :--- | :--- | :--- | :--- |
| 1 | Phạm Trần Anh Quân | Member 1 — File gathering & tree building | `gatherer.py`, `hierarchy.py`, `pipeline_m2.py`, `m2_contract.py` | [Chapter 9](./09_parsing.ipynb) |
| 2 | Lê Phạm Minh Thu | Member 2 — Content standardization | `cleaner.py`, `normalizer.py`, `sentence_splitter.py`, `leaf_extractor.py`, `latex_scan.py` | [Chapter 10](./10_standardization.ipynb) |
| 3 | Lương Gia Bảo | Member 3 — References & BibTeX | `reference_parser/` (`bibitem_parser`, `bibtex_converter`, `dedup_bibtex`, `citation_updater`), `fetch_bbl.py` | [Chapter 11](./11_references.ipynb) |
| 4 | Trần Thị Ngọc Trâm | Member 4 — Element IDs, validation & performance | `dedup_elements.py`, `validate_m2.py`, `statistics_m2.py`, `benchmark_m2.py`, `group_benchmark_m2.py` | [Chapters 12](./12_results.ipynb)–[14](./14_validation.ipynb) |
| 5 | Nguyễn Thành Phát | Member 5 — Jupyter Book & documentation | this part of the book, `export_report_data_m2.py`, `README.md` | the whole part |

As in Milestone 1, the tables and figures label each of the five ID ranges with the first name of the member it was
assigned to (Quan, Bao, Phat, Thu, Tram), and call it a *range*.

## 2. Objectives

Milestone 1 stored the LaTeX source of every version of each paper, but in raw form: several files, many formatting
commands, bibliographies written in many styles. Milestone 2 turns that corpus into structured data that Milestone 3
can use:

1. **Hierarchical parsing:** for each version, find the root file, merge the files called by `\input`/`\include` in
   reading order, and build the tree *document → section → subsection → paragraph → sentence, formula, figure*.
2. **Standardization:** remove commands used only for layout, bring every formula to one form, and split sentences
   correctly even around formulas, abbreviations and decimal numbers.
3. **References:** convert `\bibitem` entries, `.bib` entries and `.bbl` files to one BibTeX form.
4. **Two-level deduplication:** identical content across versions shares one ID; duplicate references are merged
   (field union) and every `\cite` is renamed to one canonical key.
5. **Validation and performance measurement** on a CPU-only Google Colab runtime.

## 3. Pipeline

```{mermaid}
flowchart LR
    A["M1 corpus<br>corpus/&lt;id&gt;/vN/*.tex, .bib, .bbl"] --> B["gatherer<br>root file + \input"]
    B --> C["reference_parser<br>\bibitem, .bib, .bbl → BibTeX<br>deduplication, \cite renaming"]
    B --> D["cleaner → normalizer<br>remove formatting, normalize math"]
    C --> D
    D --> E["hierarchy + leaf_extractor<br>tree and leaf elements"]
    E --> F["dedup_elements<br>element_id shared across versions"]
    F --> G["Parquet<br>elements · hierarchy · bibtex"]
    C --> G
    G --> H["validate_m2 · statistics_m2 · benchmark_m2"]
```

`src/pipeline_m2.py` runs these steps for each paper, in several processes, stores the result of each paper in
`corpus/<id>/parsed/` and then writes the three Parquet tables. Papers already parsed by the same code version are
skipped on a re-run, so an interrupted run can resume.

## 4. Reading the next chapters

- [Chapter 9](./09_parsing.ipynb) and [Chapter 10](./10_standardization.ipynb): how the trees are built and the
  content is standardized.
- [Chapter 11](./11_references.ipynb): references, BibTeX and reference deduplication.
- [Chapter 12](./12_results.ipynb): parsing success rate, elements and references before and after deduplication.
- [Chapter 13](./13_performance.ipynb): wall time, mean time per paper, peak RAM, output size.
- [Chapter 14](./14_validation.ipynb): automatic checks and limitations.

Every table and figure is computed at build time from the aggregated tables in `data/m2/`, written by
`src/export_report_data_m2.py` of the code repository from the results of the Colab run. The book contains no text
of the papers themselves.
