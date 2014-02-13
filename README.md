
1. Select all multi-polygons
Check for holes:
2. For each polygon part, check if it is completely contained by another part (i.e. it is a hole)
If a hole is found: 
3. pick a point the hole. Intersect the multi-polygon with a line that passes through the hole.
4. For each resulting multi-polygon recursively check for holes
5. Replace the parent multi-polygon with the resulting pieces

