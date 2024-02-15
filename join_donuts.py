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

import numpy as np
import shapely.geometry as sg
import fiona
import sys

VERBOSE = True

def dprint(s):
    if VERBOSE:
        print(s)

def closest_pt(pt, ptset):
    """"""
    
    dist2 = np.sum(np.asarray((ptset - pt)) ** 2,1)
    minidx = np.argmin(dist2)
    return minidx

def cw_perpendicular(pt, norm=None):
    """"""
    d = np.sqrt((pt**2).sum()) or 1
    if norm is None:
        return np.array([pt[1],-pt[0]])
    return np.array([pt[1],-pt[0]]) / d * norm

def lazy_short_join_gap(exter, inter, refpt, gap=0.000001):
    """"""
    exIdx = closest_pt(refpt,exter)
    inIdx = closest_pt(exter[exIdx],inter)
    excwgap = exter[exIdx]+cw_perpendicular(inter[inIdx]-exter[exIdx],gap)
    incwgap = inter[inIdx]+cw_perpendicular(exter[exIdx]-inter[inIdx],gap)
    out = np.vstack((exter[:exIdx],excwgap,inter[inIdx:-1],inter[:inIdx],incwgap,exter[exIdx:]))
    out[-1]=out[0]
    return out

def lazy_short_join_poly(poly):
    """"""
    if len(poly.interiors):
        ex = np.asarray(poly.exterior.coords)
        for inter in poly.interiors:
            inArr = np.asarray(inter.coords)
            ex = lazy_short_join_gap(ex, inArr, np.asarray(inter.centroid.coords))
        poly = sg.Polygon(ex)
    return poly

def lazy_short_join_multipoly(shape, correct_errors=True):
    """"""
    parts = []
    if shape.geom_type == "MultiPolygon":
        for p in shape.geoms:
            parts.append(lazy_short_join_poly(p))
    elif shape.geom_type == "Polygon":
        parts = [lazy_short_join_poly(shape)]

    if correct_errors:
        corrected = []
        for poly in parts:
            if poly.is_empty:
                dprint("warning: removed null geometry")
            else:
                if not poly.is_valid:
                    corrected.extend(lazy_short_join_multipoly(poly.buffer(0.0), False))
                else:
                    corrected.append(poly)
        return corrected
    else:
        for poly in parts:
            if poly.is_empty:
                parts.remove(poly)
                dprint("warning: removed null geometry")
            elif not poly.is_valid:
                dprint("warning: did not correct invalid geometry")
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
    print("Usage:\tjoin_donuts.py <shape.shp> <outfile.shp>")


if __name__ == "__main__":
    if len(sys.argv)==3:
        shp = sys.argv[1]
        out_shp = sys.argv[2]
        join_donuts(shp, out_shp)
    else:
        print_usage()
