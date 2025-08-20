// 02 — Counts by key label
// Edit the list as needed to include/exclude labels.
UNWIND ['Cell_cluster','Cell','Assay','Biological_process','Cellular_component','Dataset','Gene','Protein',
        'Disease','Multicellular_anatomical_structure','Developmental_stage','Race'] AS L
CALL {
  WITH L
  MATCH (n)
  WHERE L IN labels(n)
  RETURN count(n) AS n
}
RETURN L AS label, n
ORDER BY n DESC;
