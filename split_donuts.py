#!/usr/bin/env python
"""
The MIT License (MIT)

Copyright (c) 2014 Francis Gassert

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

Updated 2021-03-19 for Python 3 by Andy Anderson.
"""

import shapely.geometry as sg
import shapely.validation as validation
import fiona
import sys


def split_horiz_by_point(polygon, point):
    """"""
    assert polygon.geom_type == "Polygon" and point.geom_type == "Point"
    nx, ny, xx, xy = polygon.bounds
    if point.x < nx or point.x > xx:
        return [polygon]

    lEnv = sg.LineString([(nx,      ny), (point.x, xy)]).envelope
    rEnv = sg.LineString([(point.x, ny), (xx,      xy)]).envelope
    
    try:
        return [polygon.intersection(lEnv), polygon.intersection(rEnv)]
    except Exception as e:
        print("Geometry error: %s" % validation.explain_validity(polygon))
        return [polygon.buffer(0)]

def check_split_multipoly(shape):
    """"""
    parts = []
    if shape.type == "MultiPolygon":
        for p in shape.geoms:
            parts.extend(check_split_multipoly(p))
    elif shape.type == "Polygon":
        if len(shape.interiors):
            pt = shape.interiors[0].centroid
            halves = split_horiz_by_point(shape, pt)
            for p in halves:
                parts.extend(check_split_multipoly(p))
        else:
            parts = [shape]
    return parts

def print_usage():
    """"""
    print("Usage:\tsplit_donuts.py <shape.shp> <outfile.shp>")


def split_donuts(shp, out_shp):
    """"""
    with fiona.open(shp) as source:
        with fiona.open(out_shp,'w',
                        driver=source.driver,
                        crs=source.crs,
                        schema=source.schema) as outfile:
            for item in source:
                shape = sg.shape(item['geometry'])
                parts = check_split_multipoly(shape)
                for p in parts:
                    outfile.write(
                        {'id':-1,
                         'properties':item['properties'],
                         'geometry':sg.mapping(p)})
        

if __name__ == "__main__":
    if len(sys.argv)==3:
        shp = sys.argv[1]
        out_shp = sys.argv[2]
        split_donuts(shp, out_shp)
    else:
        print_usage()
    
