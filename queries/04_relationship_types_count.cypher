// 04 — Relationship types by count
MATCH ()-[r]-()
RETURN type(r) AS rt, count(*) AS c
ORDER BY c DESC;
