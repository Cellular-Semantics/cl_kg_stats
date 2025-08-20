// 06 — Top diseases across clusters
MATCH (c:Cell_cluster)-[:disease]->(d)
WITH d, count(DISTINCT c) AS clusters
RETURN d.label AS disease, clusters
ORDER BY clusters DESC LIMIT 20;
