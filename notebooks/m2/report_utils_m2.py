"""Helpers shared by the Milestone 2 report notebooks.

Every table and figure of the Milestone 2 part is computed at build time from the small aggregated
files in data/m2/, written by the code repository's src/export_report_data_m2.py. Nothing here reads
the parsed text or the Parquet tables.

While data/m2/ has not been exported yet, ready() shows a note and returns False, and the chapters
show their text without numbers, so the book still builds.
"""

from __future__ import annotations

import json
import sys
from functools import lru_cache
from pathlib import Path

import pandas as pd
from IPython.display import HTML, display

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # notebooks/report_utils.py of Milestone 1
from report_utils import COLORS, human_bytes, human_seconds, pct, show, table  # noqa: E402,F401

ORDER = ["Quan", "Bao", "Phat", "Thu", "Tram"]  # same order as Milestone 1
KIND_LABELS = {"document": "Version root", "heading": "Heading", "paragraph": "\\paragraph",
               "list": "List", "item": "List item", "sentence": "Sentence", "formula": "Formula",
               "figure": "Figure / table"}
# export_report_data_m2.py groups gatherer.py's messages by keyword; these labels say what the messages mean
PROBLEM_LABELS = {
    "Root file not determined": "Several root candidates, or a guessed root file",
    "Character encoding error": "File not in UTF-8, read as Latin-1",
}
ID_COLUMNS = {c: str for c in ("arxiv_id", "run_id")}  # 2601.18060 must not lose its last zero


def data_dir() -> Path | None:
    """data/m2/ of the book, found from the notebook's working directory; None before the export."""
    for folder in [Path.cwd(), *Path.cwd().parents]:
        candidate = folder / "data" / "m2"
        if (candidate / "meta.json").is_file():
            return candidate
    return None


def ready() -> bool:
    """True when data/m2/ holds an export; otherwise say so in the page."""
    if data_dir() is not None:
        provenance()
        return True
    # HTML rather than Markdown: MyST shows a Markdown output as raw text
    display(HTML(
        "<blockquote><p><strong>No data yet.</strong> <code>data/m2/</code> has not been exported. The tables and "
        "figures of this chapter appear once the group runs <code>src/export_report_data_m2.py</code> on the "
        "Milestone 2 results and commits <code>data/m2/</code>.</p></blockquote>"))
    return False


@lru_cache(maxsize=None)
def _load(name: str) -> pd.DataFrame:
    folder = data_dir()
    for path in (folder / f"{name}.csv.gz", folder / f"{name}.csv"):
        if path.is_file():
            try:
                return pd.read_csv(path, low_memory=False, dtype=ID_COLUMNS)
            except pd.errors.EmptyDataError:
                return pd.DataFrame()
    raise FileNotFoundError(f"{name}.csv(.gz) is missing in {folder}: re-run export_report_data_m2.py")


def load(name: str) -> pd.DataFrame:
    """One exported table, e.g. load('papers') reads data/m2/papers.csv.gz (a copy, safe to modify)."""
    return _load(name).copy()


def meta() -> dict:
    return json.loads((data_dir() / "meta.json").read_text(encoding="utf-8"))


def ordered(df: pd.DataFrame, column: str = "member") -> pd.DataFrame:
    """Rows in the order of the ranges, then the others (e.g. 'group')."""
    rank = {name: i for i, name in enumerate(ORDER)}
    return df.sort_values(column, key=lambda s: s.map(lambda v: rank.get(v, len(rank)))).reset_index(drop=True)


def members() -> pd.DataFrame:
    """group_benchmark_m2's row per range, without the 'group' row."""
    df = load("members")
    return ordered(df[df["member"] != "group"])


def group() -> pd.Series:
    df = load("members")
    return df[df["member"] == "group"].iloc[0]


def metric(name: str, member: str | None = None) -> float:
    """A metric of summary_statistics_m2.csv: one range's value, or the sum over the ranges (counts only)."""
    stats = load("statistics")
    rows = stats[stats["metric"] == name]
    if member is not None:
        rows = rows[rows["member"] == member]
    values = pd.to_numeric(rows["value"], errors="coerce")
    return float(values.sum()) if values.notna().any() else float("nan")


def metric_table(names: dict[str, str]) -> pd.DataFrame:
    """One column per range, one row per metric (label -> metric name), plus the sum."""
    rows = []
    for label, name in names.items():
        row = {"Metric": label}
        for m in members()["member"]:
            v = metric(name, m)
            row[m] = "–" if pd.isna(v) else f"{v:,.0f}"
        total = metric(name)
        row["Group"] = "–" if pd.isna(total) else f"{total:,.0f}"
        rows.append(row)
    return pd.DataFrame(rows)


def num(x, digits: int = 0) -> str:
    return "–" if x is None or pd.isna(x) else f"{x:,.{digits}f}"


def percent(value) -> str:
    """A value already in percent (e.g. 21.3 -> '21.30%')."""
    return "–" if value is None or pd.isna(value) else f"{float(value):.2f}%"


def secs(s) -> str:
    """Short durations with enough decimals (a paper takes well under a second); long ones as human_seconds."""
    if s is None or pd.isna(s):
        return "–"
    return f"{s:.3f} s" if s < 10 else human_seconds(s)


def provenance() -> None:
    """Where the numbers of a chapter come from."""
    m = meta()
    commits = ", ".join(f"<code>{c[:10]}</code>" for c in m.get("commits") or []) or "unknown"
    display(HTML(f"<p><small>Data source: <code>data/m2/</code>, exported at {m['exported_at']} "
                 f"from the results of {len(m['members'])} ranges ({', '.join(m['members'])}); "
                 f"code commit {commits}.</small></p>"))
