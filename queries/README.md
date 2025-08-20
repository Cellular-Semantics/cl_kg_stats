# Queries

This folder contains the Cypher queries used to generate summary statistics for **CL_KG**.  
They are numbered to indicate the order in which they are typically executed when building the release-note report.

Each file contains a single self-contained query. The output of these queries is consumed by the reporting script in `scripts/`.

---

## Query Index

### 01_totals.cypher
Returns the **total number of nodes and relationships** in the graph.

### 02_counts_by_label.cypher
Counts nodes by **key label** (Cell_cluster, Cell, Dataset, Gene, Protein, etc.).  
Useful for tracking growth of the graph across releases.

### 03_avg_degree_by_label.cypher
Computes the **average degree (number of relationships)** for selected node labels.  
Highlights how richly connected different node types are.

### 04_relationship_types_count.cypher
Lists all **relationship types** in the graph and counts how many of each exist.  
Sorted by frequency, descending.

### 05_top_tissues.cypher
Top 20 **tissues** annotated across `Cell_cluster` nodes.

### 06_top_diseases.cypher
Top 20 **diseases** annotated across `Cell_cluster` nodes.

### 07_assay_types.cypher
Distribution of **assay types** used across clusters.

### 08_development_stages.cypher
Distribution of **developmental stages** annotated across clusters.

### 09_provenance_summary.cypher
Summarizes **how many datasets** exist and **how many clusters** have dataset sources.  
Acts as a quick check on dataset coverage.

### 10_top_datasets_by_clusters.cypher
Lists datasets ranked by the number of clusters linked to them.  
Includes an alternative version (commented) that groups by **Dataset node ID** instead of title to avoid collapsing nodes without a title.

---

## Usage Notes

- The queries are written for Neo4j 4.4.x syntax and tested on version 4.4.44.
- You can run them individually in Neo4j Browser, or execute them programmatically via the `scripts/generate_report.py` script.  
- Outputs are typically formatted into Markdown tables for inclusion in release notes.  
- To add a new query, create a new file with the next available number (e.g. `11_new_metric.cypher`) and update this README with a short description.
