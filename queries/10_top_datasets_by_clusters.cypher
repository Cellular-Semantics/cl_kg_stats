// 10 — Top datasets by #clusters
MATCH (c:Cell_cluster)-[:has_source]->(d:Dataset)
RETURN d.title[0] AS dataset, count(DISTINCT c) AS clusters
ORDER BY clusters DESC LIMIT 20;
