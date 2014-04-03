GIS utility to split complex multipolygons into simple polygons (closed rings without holes or multiple parts)

**Dependencies**
- [Shapely](https://pypi.python.org/pypi/Shapely/) and [Fiona](https://pypi.python.org/pypi/Fiona)
- [GDAL/OGR](http://www.gdal.org/ogr/)

**Usage:** `split_donuts.py <in_shp> <out_shp>`

**-or-**

**Usage:** `join_donuts.py <in_shp> <out_shp>`

**split_donuts.py works as follows**

1. For each feature in a collection
2. If it is a multipolygon split it into separate polygons
3. For each polygon, check if it has any interior rings (holes)
4. Pick a point in the hole. Return the left half and right half of the polygon.
5. For each resulting polygon recursively check for holes
6. Return the resulting polygons

**join_donuts.py works as follows**

1. For each feature in a collection
2. If it is a multipolygon split it into separate polygons
3. For each polygon, check if it has any interior rings (holes)
4. For each interior ring, find the closest point in the exterior ring to the centroid of the interior ring
5. Then find the closest point in the interior ring to the point we just found
6. Join the two rings together such that an edge now links the closest point in the exterior to the closest point in the interior, and treat this as the new exterior ring.
7. Repeat steps 4-6 for the remaining interior rings with the new exterior ring
8. Return the resulting polygons

**tests**

`tests.py`

e.g. multip.shp is split as follows:
![multip.shp](https://raw.github.com/fgassert/split_donuts/master/multip.png) -> 
![out.shp](https://raw.github.com/fgassert/split_donuts/master/out.png)
