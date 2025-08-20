#!/usr/bin/env python3
"""
Generate a Markdown report from Cypher queries for CL_KG.

- Discovers and executes all `*.cypher` files in queries/, in numeric/alpha order
- Extracts a human-friendly section title from the first comment line (// ...),
  or falls back to the filename
- Renders `report_templates/release_notes.md.j2` with the query outputs

Tested with Neo4j 4.4.44 and neo4j Python driver >= 4.4.
"""
import argparse
import glob
import os
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Tuple

from neo4j import GraphDatabase
from jinja2 import Environment, FileSystemLoader, select_autoescape

FIXED_URI = "neo4j://172.27.24.69:7687"
TITLE_LINE_RE = re.compile(r"^\s*//\s*(?P<title>.+?)\s*$")
SLUG_RE = re.compile(r"[^a-z0-9]+")


def slugify(s: str) -> str:
    s = s.lower().strip()
    s = SLUG_RE.sub("-", s).strip("-")
    return s or "section"


def render_table_md(columns, rows) -> str:
    lines = []
    # header
    lines.append("| " + " | ".join(columns) + " |")
    # separator
    lines.append("| " + " | ".join(["---"] * len(columns)) + " |")
    # rows
    for row in rows:
        vals = [str(row.get(c, "")) for c in columns]
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines) + "\n"


def write_section_page(out_dir: str, section, index: int) -> dict:
    """Write a standalone .md page for a section; return metadata (slug, relpath)."""
    title = section["title"]
    file = section["file"]
    columns = section["columns"]
    rows = section["rows"]

    slug = slugify(section["title"])
    out_dir_path = Path(out_dir)
    out_dir_path.mkdir(parents=True, exist_ok=True)
    page_path = out_dir_path / f"{slug}.md"

    if not rows:
        body = "_No rows returned._\n"
    else:
        body = "\n" + render_table_md(columns, rows) + "\n"

    content = f"# {title}\n\n" \
              f"<sub><em>Source: {file}</em></sub>\n\n" \
              f"{body}"

    page_path.write_text(content, encoding="utf-8")
    return {"slug": slug, "relpath": str(page_path)}


def discover_queries(query_dir: str) -> List[str]:
    files = sorted(glob.glob(os.path.join(query_dir, "*.cypher")))
    return files


def extract_title(query_text: str, fallback: str) -> str:
    for line in query_text.splitlines():
        m = TITLE_LINE_RE.match(line)
        if m:
            return m.group("title").strip()
        if line.strip() and not line.strip().startswith("//"):
            # First non-comment content reached — stop scanning
            break
    # Fallback: prettify filename
    name = os.path.splitext(os.path.basename(fallback))[0]
    return name.replace("_", " ")


def run_query(session, query: str) -> Tuple[List[str], List[Dict[str, Any]]]:
    # Run and collect rows while keeping column order
    result = session.run(query)
    columns = list(result.keys())
    rows = [dict(record) for record in result]
    return columns, rows


def render_markdown(template_path: str, context: Dict[str, Any]) -> str:
    template_dir = os.path.dirname(template_path) or "."
    template_name = os.path.basename(template_path)

    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(enabled_extensions=(".j2",)),
    )
    tmpl = env.get_template(template_name)
    return tmpl.render(**context)


def main():
    ap = argparse.ArgumentParser(description="Generate CL_KG summary report")

    ap.add_argument(
        "--queries", default="queries", help="Directory containing .cypher files"
    )
    ap.add_argument(
        "--template", default=os.path.join("report_templates", "release_notes.md.j2")
    )
    ap.add_argument("--out", default="report.md", help="Output Markdown file path")
    args = ap.parse_args()

    queries = discover_queries(args.queries)
    if not queries:
        raise SystemExit(f"No .cypher files found under {args.queries}")

    # Authentication is disabled on this server; connect without credentials.
    driver = GraphDatabase.driver(FIXED_URI)

    sections = []
    with driver.session() as session:
        for path in queries:
            with open(path, "r", encoding="utf-8") as fh:
                qtext = fh.read()
            title = extract_title(qtext, path)
            cols, rows = run_query(session, qtext)
            sections.append(
                {
                    "file": os.path.basename(path),
                    "title": title,
                    "columns": cols,
                    "rows": rows,
                }
            )

    sections_dir = "section_pages"
    standalone_pages = []
    for i, s in enumerate(sections, start=1):
        meta = write_section_page(sections_dir, s, i)
        s["slug"] = meta["slug"]
        s["standalone_rel"] = meta["relpath"]
        standalone_pages.append(meta)

    context = {
        "generated_on": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        "sections": sections,
    }

    md = render_markdown(args.template, context)
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(md)

    print(f"Wrote {args.out} with {len(sections)} sections.")


if __name__ == "__main__":
    main()
