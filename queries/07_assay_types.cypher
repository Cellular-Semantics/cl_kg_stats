// 07 — Assay types across clusters
MATCH (c:Cell_cluster)-[:assay]->(a)
RETURN a.label AS assay, count(DISTINCT c) AS clusters
ORDER BY clusters DESC;
