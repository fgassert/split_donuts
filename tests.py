

from split_donuts import *
from shapely.ops import cascaded_union

def test_split():
    print "Split donut by interior point"
    donut = sg.Point(0, 0).buffer(2.0).difference(sg.Point(0, 0).buffer(1.0))
    center = donut.centroid
    res = split_horiz_by_point(donut, center)
    print "Parts (should be 2): %s" % len(res)
    dif = cascaded_union(res).symmetric_difference(donut).area
    print "Difference: %s" % dif

    print "Split donut by exterior point"
    side = sg.Point(4,4)
    res = split_horiz_by_point(donut, side)
    print "Parts (should be 1): %s" % len(res)
    dif = cascaded_union(res).symmetric_difference(donut).area
    print "Difference: %s" % dif

def test_check_split():
    print "Check if a donut needs to be split"
    donut = sg.Point(0, 0).buffer(2.0).difference(sg.Point(0, 0).buffer(1.0))
    res = check_split_multipoly(donut)
    print "Parts (should be 2): %s" % len(res)
    dif = cascaded_union(res).symmetric_difference(donut).area
    print "Difference: %s" % dif


    print "Check if a multipoly needs to be split"
    multi = sg.MultiPoint([(0, 0),(4, 0)]).buffer(2.0)
    res = check_split_multipoly(multi)
    print "Parts (should be 2): %s" % len(res)
    dif = cascaded_union(res).symmetric_difference(multi).area
    print "Difference: %s" % dif


    print "Check if a complex multipoly needs to be split"
    cx = sg.MultiPoint([(0, 0),(4, 0)]).buffer(2.0).difference(sg.Point(0, 0).buffer(1.0))
    res = check_split_multipoly(cx)
    print "Parts (should be 3): %s" % len(res)
    dif = cascaded_union(res).symmetric_difference(cx).area
    print "Difference: %s" % dif

def test_split_shp():
    print "splitting multip.shp"
    split_donuts("multip.shp","out.shp")
    with fiona.open("out.shp") as source:
        print "Parts (should be 7): %s" % len(source)

if __name__ == "__main__":
    
    test_split()
    test_check_split()
    test_split_shp()
