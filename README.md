GIS utility to split complex multipolygons into simple polygons (closed rings without holes or multiple parts)

**Dependencies**
- [Shapely](https://pypi.python.org/pypi/Shapely/) and [Fiona](https://pypi.python.org/pypi/Fiona)
- [GDAL/OGR](http://www.gdal.org/ogr/)

**Usage:** `split_donuts.py <in_shp> <out_shp>`

**Works as follows**

1. For each feature in a collection
2. If it is a multipolygon split it into separate polygons
3. For each polygon, check if it has any interior rings (holes)
3. Pick a point in the hole. Return the left half and right half of the polygon.
4. For each resulting polygon recursively check for holes
5. Return the resulting polygons

**tests**

`tests.py`

e.g. multip.shp is split as follows:
![multip.shp](https://raw.github.com/fgassert/split_donuts/master/multip.png) -> 
![out.shp](https://raw.github.com/fgassert/split_donuts/master/out.png)
