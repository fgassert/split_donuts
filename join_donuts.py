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
"""

import numpy as np
import numexpr as ne
import shapely.geometry as sg
import fiona
import sys

def closest_pt(pt, ptset):
    """"""
    dist2 = np.sum((ptset - pt) ** 2,1)
    minidx = np.argmin(dist2)
    return minidx

def closest_pt_ne(pt, ptset):
    """"""
    dist2 = ne.evaluate("sum((ptset - pt) ** 2,1)")
    minidx = np.argmin(dist2)
    return minidx
    
def lazy_short_join(exter, inter, refpt):
    """"""
    exIdx = closest_pt_ne(refpt,exter)
    inIdx = closest_pt_ne(exter[exIdx],inter)
    return np.vstack((exter[:exIdx+1],inter[inIdx:],inter[:inIdx+1],exter[exIdx:]))

def lazy_short_join_poly(poly):
    """"""
    if len(poly.interiors):
        ex = np.asarray(poly.exterior)
        for inter in poly.interiors:
            inArr = np.asarray(inter)
            ex = lazy_short_join(ex, inArr, np.asarray(inter.centroid))
        return sg.Polygon(ex)
    else:
        return poly

def lazy_short_join_multipoly(shape):
    """"""
    parts = []
    if shape.type == "MultiPolygon":
        for p in shape.geoms:
            parts.append(lazy_short_join_poly(p))
    elif shape.type == "Polygon":
        parts = [lazy_short_join_poly(shape)]
    return parts

def join_donuts(shp, out_shp):
    """"""
    with fiona.open(shp) as source:
        with fiona.open(out_shp,'w',
                        driver=source.driver,
                        crs=source.crs,
                        schema=source.schema) as outfile:
            for item in source:
                shape = sg.shape(item['geometry'])
                parts = lazy_short_join_multipoly(shape)
                for p in parts:
                    outfile.write(
                        {'id':-1,
                         'properties':item['properties'],
                         'geometry':sg.mapping(p)})


def print_usage():
    """"""
    print "Usage:\tjoin_donuts.py <shape.shp> <outfile.shp>"


if __name__ == "__main__":
    if len(sys.argv)==3:
        shp = sys.argv[1]
        out_shp = sys.argv[2]
        join_donuts(shp, out_shp)
    else:
        print_usage()
