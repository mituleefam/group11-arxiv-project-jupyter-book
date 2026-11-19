"""Build the three extra tables of data/m1 that export_report_data.py does not write.

They come from the benchmark folder of the group's final Milestone 1 run
(benchmark_ms1_main/, one sub-folder per member with snapshots/*.tar.gz and
snapshot_log.csv, plus tong_ket/verified_404_withdrawn.csv):

  manual_checks.csv    versions without a source that were checked by hand on
                       arxiv.org/abs: the 134 HTTP 404 versions (all withdrawn)
                       and the 4 versions left `failed` (HTML sources)
  download_routes.csv  per member and route (Colab, WARP, Webshare): rows of
                       logs/download_log.csv and route pauses of
                       logs/arxiv_throttle_log.csv
  snapshot_log.csv     every save/restore of a snapshot archive (not part of
                       the measured crawl time)

Only small aggregates are written: no LaTeX, no titles, no proxy address.

    python tools/m1_extras.py <benchmark_ms1_main> --out data/m1
"""

from __future__ import annotations

import argparse
import csv
import io
import re
import tarfile
from collections import Counter
from pathlib import Path

CHECKED_ON = "2026-11-19"

# The 4 versions the crawler left `failed` ("gzip file holds an HTML page"):
# arXiv answered HTTP 200 with the same gzipped HTML file on each of 22 tries.
# Their abs pages show the source is HTML, not TeX.
HTML_SOURCES = {
    ("2604.05737", "v1"): "Access Paper offers HTML and HTML Source, no TeX Source: EPTCS 444 proceedings submitted as HTML",
    ("2604.08605", "v1"): "Access Paper offers HTML and HTML Source, no TeX Source: workshop proceedings submitted as HTML",
    ("2601.14107", "v1"): "Access Paper offers HTML and HTML Source, no TeX Source: ICRC2025 contributions submitted as HTML",
    ("2601.17022", "v1"): "Access Paper offers View PDF only, no TeX Source: the source stored by arXiv is a 999 KB gzipped HTML file",
}
WITHDRAWN_EVIDENCE = "The Submission history on the abstract page marks this version as (withdrawn)"


def member_of(folder: Path) -> str:
    return folder.name.split("_")[0]


def last_logs(snapshots: Path, names: tuple[str, ...]) -> dict[str, bytes]:
    """The newest copy of each log file in the incremental archives (a log is
    appended to, so the last archive that holds it has all its rows)."""
    found: dict[str, bytes] = {}
    for archive in sorted(snapshots.glob("*.tar.gz")):
        with tarfile.open(archive, "r:gz") as tar:
            for info in tar:
                if info.isfile() and info.name in names:
                    found[info.name] = tar.extractfile(info).read()
    return found


def route_name(text: str) -> str:
    if "Webshare" in text:
        return "Webshare"
    for name in ("Colab", "WARP", "AWS"):
        if name in text:
            return name
    return "other"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("benchmark_dir", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    members = sorted(p for p in args.benchmark_dir.iterdir() if (p / "snapshots").is_dir())

    # manual checks
    rows = []
    verified = args.benchmark_dir / "tong_ket" / "verified_404_withdrawn.csv"
    with verified.open(encoding="utf-8-sig", newline="") as stream:
        for r in csv.DictReader(stream):
            rows.append([r["member"], r["arxiv_id"], r["version"], "not_found", "withdrawn",
                         WITHDRAWN_EVIDENCE, CHECKED_ON])
    for folder in members:
        report = folder / "validation_report.csv"
        with report.open(encoding="utf-8-sig", newline="") as stream:
            failed = {(r["arxiv_id"], r["version"]) for r in csv.DictReader(stream)
                      if "failed" in (r.get("error_message") or "")}
        for key, evidence in HTML_SOURCES.items():
            if key in failed:
                rows.append([member_of(folder), *key, "failed", "html_source", evidence, CHECKED_ON])
    with (args.out / "manual_checks.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["member", "arxiv_id", "version", "crawl_status", "finding", "evidence", "checked_on"])
        writer.writerows(rows)
    print(f"manual_checks.csv: {len(rows)} rows, {dict(Counter(r[4] for r in rows))}")

    # routes and snapshot times
    route_rows, snap_rows = [], []
    for folder in members:
        name = member_of(folder)
        logs = last_logs(folder / "snapshots", ("logs/download_log.csv", "logs/arxiv_throttle_log.csv"))
        downloads = Counter(r["route"] for r in csv.DictReader(io.StringIO(
            logs["logs/download_log.csv"].decode("utf-8"))))
        pauses = Counter()
        if "logs/arxiv_throttle_log.csv" in logs:
            for r in csv.DictReader(io.StringIO(logs["logs/arxiv_throttle_log.csv"].decode("utf-8"))):
                if r["event"] == "route_pause":
                    via = re.search(r"via (.+)$", r["reason"] or "")
                    pauses[route_name(via.group(1) if via else "")] += 1
        for route in sorted(set(downloads) | set(pauses)):
            route_rows.append([name, route, downloads.get(route, 0), pauses.get(route, 0)])
        with (folder / "snapshot_log.csv").open(encoding="utf-8-sig", newline="") as stream:
            for r in csv.DictReader(stream):
                snap_rows.append([name, r["time"], r["step"], r["action"], r["archive"], r["seconds"], r["bytes"]])
        print(f"{name}: downloads {dict(downloads)}, route pauses {dict(pauses)}")
    with (args.out / "download_routes.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["member", "route", "download_log_rows", "route_pauses"])
        writer.writerows(route_rows)
    with (args.out / "snapshot_log.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["member", "time", "step", "action", "archive", "seconds", "bytes"])
        writer.writerows(snap_rows)
    print(f"snapshot_log.csv: {len(snap_rows)} rows")


if __name__ == "__main__":
    main()
