// 11 — List all dataset titles alphabetically with row numbers
MATCH (d:Dataset)
WHERE d.title IS NOT NULL AND trim(toString(d.title[0])) <> ''
WITH DISTINCT toString(d.title[0]) AS dataset
ORDER BY dataset ASC
WITH collect(dataset) AS datasets
UNWIND range(0, size(datasets)-1) AS i
RETURN i+1 AS idx, datasets[i] AS dataset;
