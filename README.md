# cl_kg_stats

This repo generates summary statistics for the **CL_KG** Neo4j database.  
The output is a Markdown report that gets copied into the [CL_KG repo](https://github.com/<your-org>/CL_KG) and published as part of its documentation.

---

## What’s inside

- **queries/** – Cypher queries, one per file.  
- **scripts/** – `generate_report.py` runs all queries and writes `report.md`.  
- **report_templates/** – Jinja2 template that turns query results into Markdown.  
- **section_pages/** – per-query Markdown pages, generated alongside `report.md`, used for publishing in CL_KG docs.  
- **report.md** – the combined summary report (not tracked in git).  

---

## How to run it

You’ll need Python 3.10+ and [Poetry](https://python-poetry.org/).

```bash
poetry install --no-root
poetry run python scripts/generate_report.py \
  --queries queries \
  --template report_templates/release_notes.md.j2 \
  --out report.md
