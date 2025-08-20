// 05 — Top tissues across clusters
MATCH (c:Cell_cluster)-[:tissue]->(t)
WITH t, count(DISTINCT c) AS clusters
RETURN t.label AS tissue, clusters
ORDER BY clusters DESC LIMIT 20;
