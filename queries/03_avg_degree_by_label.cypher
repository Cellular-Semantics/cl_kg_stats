// 03 — Average degree by label
// Degree = total number of relationships per node (all directions/types).
UNWIND [
  'Cell_cluster','Cell','Dataset','Gene',
  'Protein','Biological_process','Cellular_component'
] AS L
CALL {
  WITH L
  MATCH (n)
  WHERE L IN labels(n)
  WITH size((n)--()) AS deg
  RETURN avg(deg) AS avg_degree
}
RETURN L AS label, round(avg_degree,2) AS avg_degree
ORDER BY avg_degree DESC;
