# data/m2 — aggregated data of Milestone 2

The notebooks of the Milestone 2 part (`notebooks/m2/`) read this folder when the book is built. It holds only
aggregated tables (counts, sizes, statuses, timings), no sentences, formulas or reference titles of the papers, so it
is committed to the book repository. Without `meta.json`, the Milestone 2 chapters still build and say there is no
data yet.

Regenerate it with the code repository's script, once `src/notebooks/m2_benchmark_colab.ipynb` has run its sections 8–11 (all
five ranges parsed, validated, counted and merged). On Colab, with Google Drive mounted:

```bash
python src/export_report_data_m2.py --results /content/drive/MyDrive/g11_m2_benchmark \
    --out <book repository>/data/m2
```

`--results` is the notebook's result folder (`RESULT_DRIVE`): one `<range>_m2.tar.gz` per range and `_merged/`. The
script reads the archives directly, without extracting them, sends no request and changes nothing in the results.

| File | Content |
| :--- | :--- |
| `meta.json` | export time, code commit, CPU and `run_id` of each range, the merge run, warnings |
| `members.csv` | `group_benchmark_m2.csv`: one row per range and the `group` row |
| `statistics.csv` | `summary_statistics_m2.csv` of each range |
| `papers.csv.gz` | one row per paper: `parse_log.csv` joined with `reference_log.csv` |
| `versions.csv.gz` | one row per version: `gathering.json` and the tree shape (nodes, depth, nodes per kind) |
| `headings.csv` | headings per level |
| `problems.csv` | problems while merging files, per kind |
| `validation_counts.csv`, `validation_issues.csv.gz` | results of `validate_m2.py` (counts per check; WARN/FAIL rows) |
| `benchmark_runs.csv` | the parsing run of each range and the merge run |
| `performance_samples.csv.gz` | RAM samples over time of those runs |
| `tables.csv` | `tables.json` of each range and of the merged tables |
| `bbl.csv` | results of `fetch_bbl.py` (when the range has `bbl_log.csv`) |
