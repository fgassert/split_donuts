#!/usr/bin/env python

import shapely.geometry as sg
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
    
    return [polygon.intersection(lEnv), polygon.intersection(rEnv)]

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
    print "Usage:\tsplit_donuts.py <shape.shp> <outfile.shp>"


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
    if len(sys.argv==3):
        shp = sys.argv[1]
        out_shp = sys.argv[2]
        split_donuts(out_shp)
    else:
        print_usage()
    
