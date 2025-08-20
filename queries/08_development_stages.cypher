// 08 — Development stages across clusters
MATCH (c:Cell_cluster)-[:development_stage]->(s)
RETURN s.label AS stage, count(DISTINCT c) AS clusters
ORDER BY clusters DESC;
