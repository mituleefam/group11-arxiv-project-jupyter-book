---
title: "Chapter 1: Introduction"
short_title: "1. Introduction"
---

> **Course:** Introduction to Data Science
> **Project:** arXiv Project
> **Team:** Group 11
> **Phase:** Milestone 1 — Data Crawling

## 1. Members and responsibilities

The group has **five members**, each leading one module of the shared pipeline. The assigned arXiv ID ranges of all five members were **crawled one after another in a single run** with the same code on Google Colab, and the data of each range is kept in a separate folder.

| No. | Full name | Main Role | Modules |
| :---: | :--- | :---: | :--- | :--- |
| 1 | `Phạm Trần Anh Quân` | Member 1 — Entry Discovery & Metadata | `discovery.py`, `metadata.py`, `main.py` |
| 2 | `Lương Gia Bảo` | Member 2 — Source Downloader & Extraction | `downloader.py`, `extractor.py`, `checkpoint.py`, `rate_limiter.py` |
| 3 | `Nguyễn Thành Phát` | Member 3 — References Crawling | `references.py`, `ref_dates_kaggle.py` |
| 4 | `Trần Thị Ngọc Trâm` | Member 4 — Data Validation & Performance | `validate.py`, `corpus_statistics.py`, `benchmark.py`, `group_benchmark.py` |
| 5 | `Lê Phạm Minh Thu` | Member 5 — Jupyter Book & Documentation | Jupyter Book repository, `README.md` |

In the tables and figures, each ID range is labelled with the first name of the member assigned to it (Quan, Bao, Phat, Thu, Tram). The actual range of each member (first ID, last ID, number of IDs) is read from the crawl data and presented automatically in [Chapter 3](./03_data_organization.ipynb).

## 2. Background

[arXiv](https://arxiv.org/) is an open repository of more than two million scientific papers. Most arXiv crawling exercises collect metadata only. This project collects the **full LaTeX sources** of the papers instead of their PDF files, because LaTeX:

1. **Preserves the hierarchical structure:** chapters, sections, lists and tables are declared explicitly in LaTeX, whereas a PDF contains only laid-out blocks of text.
2. **Preserves mathematical formulas:** formulas remain in their original LaTeX form, free of the distortion caused by text extraction from PDF.
3. **Makes citations explicit:** each `\cite{}` command points directly to a key in a `\bibitem` or a `.bib` file.

According to arXiv's documentation, about **97%** of submissions have a TeX source, while the remainder are PDF-only. For versions without TeX, an empty record is kept instead of dropping the paper, as required by the statement.

Figures account for most of the size of a source archive but are not needed by the later milestones. The crawler therefore **extracts only `.tex`, `.bib` and `.bbl` files** from each archive: figure files never enter the corpus, while the `\begin{figure}` and `\includegraphics` commands inside the `.tex` files are kept byte for byte. The `.bbl` files (pre-compiled bibliographies) are kept in addition, following the instructor's Q&A ruling: for a paper with neither a `.bib` file nor `\bibitem` entries, the `.bbl` file is the only source of its references and must not be discarded. The size reduction achieved by this approach is measured on the actual data in [Chapter 4](./04_crawling_results.ipynb).

## 3. Objectives of Milestone 1

1. **Entry discovery:** resolve the assigned arXiv ID range through the arXiv API (`id_list`), distinguish existing IDs, non-existent IDs and API errors, and determine the version list `v1, v2, …` of each paper.
2. **Metadata:** collect the title, authors, submission date, revision dates and venue of each paper.
3. **LaTeX sources:** download each version individually from `https://export.arxiv.org/src/<id>v<N>`, detect the actual format of the downloaded file, and keep only `.tex`/`.bib`/`.bbl` files with their sub-folder structure.
4. **References:** collect the reference list of each paper through the Semantic Scholar Graph API, keep every reference locally, and mark the references that carry an arXiv ID.
5. **Validation and performance measurement:** check the completeness of the corpus automatically and measure running time, RAM and disk usage on a CPU-only Google Colab runtime.
6. **Report:** generate every table and figure of this book with code at build time.

## 4. Project roadmap

```{mermaid}
flowchart LR
    A["Milestone 1<br><b>Data Crawling</b><br>TeX/Bib, metadata, references"] --> B["Milestone 2<br><b>Parsing & Standardization</b><br>hierarchy trees, BibTeX, deduplication"]
    B --> C["Milestone 3<br><b>Reference Matching</b><br>ML pipeline, MRR@5, Hugging Face"]
```

| Milestone | Main objective | Deliverables |
| :---: | :--- | :--- |
| **M1** (this part) | Collect the LaTeX sources, metadata and references of every version | The group's working corpus, M1 report |
| **M2** | Build hierarchy trees, standardize the content, convert `\bibitem` entries to BibTeX, deduplicate across versions | Tables `elements`, `hierarchy`, `bibtex`, M2 report |
| **M3** | Match BibTeX entries with references that carry an arXiv ID, evaluated with MRR@5 | Hugging Face dataset, A2 poster |

Milestone 1 has no data submission: the corpus is kept by the group as the input of Milestones 2 and 3.

## 5. Structure of the Milestone 1 report

- [Chapter 2](./02_methodology.ipynb): how the crawler works, and the tools and libraries used.
- [Chapter 3](./03_data_organization.ipynb): organization of the corpus and discovery results.
- [Chapter 4](./04_crawling_results.ipynb): the statistics required by the statement.
- [Chapter 5](./05_performance.ipynb): running time, RAM and disk usage.
- [Chapter 6](./06_errors_limitations.ipynb): validation results, remaining errors and limitations.
- [Chapter 7](./07_conclusion.md): conclusion.

Source code: [group11-arxiv-project](https://github.com/mituleefam/group11-arxiv-project).
