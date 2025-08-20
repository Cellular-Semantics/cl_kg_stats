// 09 — How many datasets and clusters with sources?
MATCH (c:Cell_cluster)-[:has_source]->(d:Dataset)
RETURN count(DISTINCT d) AS datasets, count(DISTINCT c) AS clusters_with_source;
