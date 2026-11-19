# data/m1 — aggregated data of Milestone 1

The Milestone 1 notebooks read their data from this folder when the book is built. The folder holds only aggregated
tables (counts, sizes, statuses, times), with no LaTeX content and no reference titles, so it is committed to the book
repository.

It is regenerated with a script of the code repository (run after every member has finished crawling and has run
`validate.py --finished` on their folder; the script recomputes the statistics itself):

```bash
python src/export_report_data.py m1=<DATA_M1> m2=<DATA_M2> m3=<DATA_M3> m4=<DATA_M4> m5=<DATA_M5> --out <mst1-book>/data/m1
```

| File | Content |
| :--- | :--- |
| `meta.json` | Export time, code commit, member names, warnings |
| `members.csv` | One row per member and a `group` row (from `group_benchmark.py`) |
| `statistics.csv` | The metrics of `corpus_statistics.py`, per member |
| `papers.csv.gz` | One row per ID: discovery, metadata, references |
| `versions.csv.gz` | One row per version: status, format, sizes, times |
| `run_log.csv` | Time of each stage of each invocation |
| `benchmark_runs.csv` | Every `benchmark.py` invocation |
| `performance_samples.csv.gz` | RAM and disk samples over time |
| `validation_counts.csv`, `validation_issues.csv` | Results of `validate.py` |

The three files below are not written by `export_report_data.py` but by `tools/m1_extras.py` of the book repository,
from the benchmark folder of the main run (`benchmark_ms1_main/`: each member's `.tar.gz` snapshots and
`snapshot_log.csv`, plus `tong_ket/verified_404_withdrawn.csv`):

```bash
python tools/m1_extras.py <benchmark_ms1_main> --out data/m1
```

| File | Content |
| :--- | :--- |
| `manual_checks.csv` | Versions without a source checked by hand on `arxiv.org/abs`: 404 versions (withdrawn) and `failed` versions (HTML source) |
| `download_routes.csv` | Per member and route (Colab, WARP, Webshare): rows of `download_log.csv` and route pauses in `arxiv_throttle_log.csv` |
| `snapshot_log.csv` | Every snapshot save and restore (outside the crawler's wall time) |
