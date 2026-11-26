---
title: "Chapter 7: Milestone 1 Conclusion"
short_title: "7. Conclusion"
---

## 1. Achievements

The group built a reproducible crawling pipeline. The arXiv ID ranges of all five members were crawled one after another with the same code on a CPU-only Google Colab runtime, each range in its own data folder:

- **Discovery and metadata** through the arXiv API: every assigned ID is resolved, the version list of each paper is determined, and the metadata is stored with the columns of the `papers` table (title, authors, submission date, revision dates, venue).
- **LaTeX sources of every version** from `export.arxiv.org/src/<id>v<N>`: the actual file format is detected, only `.tex`/`.bib`/`.bbl` files are extracted with their relative paths, and an empty record is kept for PDF-only versions and versions without TeX.
- **References** through the Semantic Scholar Graph API: every reference is kept in `references_all.json`, and the references with an arXiv ID are separated into `references.json`, ready to become the `references` table in Milestone 3.
- **Reliability:** the request limits of arXiv and Semantic Scholar are respected. Requests to arXiv travel over several routes (Colab, WARP, Webshare); a refused route pauses on its own while the others continue, without raising the overall request pace. The crawler retries in passes, checkpoints every version, saves a snapshot to Drive after each step, and resumes after a Colab disconnection without downloading completed work again.
- **Validation and measurement:** `validate.py` checks the whole corpus, `corpus_statistics.py` computes the statistics, and `benchmark.py` measures time, RAM and disk usage on a CPU-only Colab runtime.

The concrete figures (papers crawled successfully, success rate, size before and after removing figures, average number of references, time, RAM and disk usage) are computed at build time in [Chapter 4](./04_crawling_results.ipynb) and [Chapter 5](./05_performance.ipynb).

## 2. Remaining limitations

The complete list, with the count of each case, is given in [Chapter 6](./06_errors_limitations.ipynb). In summary:

- Some versions have no TeX source: withdrawn versions (arXiv answers HTTP 404; every case was reviewed and confirmed as withdrawn), PDF-only versions, and a few HTML submissions. These versions are recorded, not skipped. The HTML submissions and one PDF with an irregular header remain in the `failed` state because `extractor.py` does not recognize them.
- Semantic Scholar has not yet indexed some recent papers, and for a few others it lists references without sharing them. Reference metadata is therefore limited to what Semantic Scholar provides.
- The ID ranges were crawled one after another on a single Colab runtime. Because of the 12-hour limit, the run spanned several sessions and resumed from snapshots, so the running time is reported per step (invocation) and summed, rather than as one continuous run. The parts outside this sum (snapshot saving and restoring, a step interrupted by a runtime failure) are measured separately in [Chapter 5](./05_performance.ipynb).

## 3. Preparation for Milestone 2

The Milestone 1 corpus is the direct input of Milestone 2:

- The sub-folder structure of each version is preserved, so `\input`/`\include` commands still resolve when the compilation path is reconstructed.
- The `.tex` files are unmodified and keep `\begin{figure}`, `\cite` and `\bibitem`, which are needed to build hierarchy trees and extract BibTeX entries.
- The `.bbl` files are kept for papers without a `.bib` file, so that Milestone 2 can still recover their bibliographies.
- `references_all.json` and `references.json` form the candidate pool for matching BibTeX entries in Milestone 3.
