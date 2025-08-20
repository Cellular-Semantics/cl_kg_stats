// 01 — Global totals
// Returns total nodes and relationships in the graph.
MATCH (n) WITH count(n) AS nodes
MATCH ()-[r]->() RETURN nodes, count(r) AS relationships;
