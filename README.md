# arXiv Project — Group 11: Jupyter Book

Report of the project, written with [Jupyter Book 2](https://jupyterbook.org) (MyST). The crawler source code is in
[group11-arxiv-project](https://github.com/mituleefam/group11-arxiv-project).

```text
myst.yml                    book configuration and table of contents (Milestone 1, later Milestone 2)
index.md                    home page
notebooks/                  chapters; 01 and 07 are Markdown, 02–06 are notebooks
notebooks/report_utils.py   shared helpers: reading data/m1/, number formatting, plotly figures
data/m1/                    aggregated data written by src/export_report_data.py of the code repository
tools/m1_extras.py          builds 3 more tables of data/m1 (manual checks, routes, snapshots) from the benchmark folder
.github/workflows/deploy.yml  builds the book (executing the notebooks) and publishes it on GitHub Pages
```

## Building locally

```bash
python -m venv .venv_book
.venv_book\Scripts\activate            # macOS/Linux: source .venv_book/bin/activate
pip install -r requirements.txt
jupyter book start --execute           # preview at http://localhost:3000
jupyter book build --html --execute    # writes _build/html
```

Node.js is required (Jupyter Book 2 offers to install it if missing). Activate the virtual environment first so that
the `jupyter` command is on the PATH; otherwise `--execute` fails with *Could not load Jupyter session manager*.

## Updating the data

Run `src/export_report_data.py` of the code repository on the data folders of all five members, with `--out` pointing
to `data/m1/` of this repository; then run `tools/m1_extras.py` on the benchmark folder, and commit `data/m1/`.
See `data/m1/README.md`.
